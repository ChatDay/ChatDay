from django.test import TestCase
from .models import Topic,Message
from chat.task import clear_chat_and_update_topic, save_messages_to_db
from celery.result import AsyncResult
import redis
from unittest.mock import patch

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(host='redis', port=6379, db=1, decode_responses=True)

class TopicModelTest(TestCase):
    def setUp(self):
        # 테스트용 데이터 준비
        self.topic = Topic.objects.create(text="오늘의 목표는?")
        self.chat_message = Message.objects.create(content="Hello!", topic=self.topic)

    def test_topic_creation(self):
        # 주제 생성 테스트
        topic = Topic.objects.get(id=self.topic.id)
        self.assertEqual(topic.text, "오늘의 목표는?")  # 주제 텍스트 확인

    def test_clear_chat_on_topic_update(self):
        # 채팅 기록 삭제 테스트
        Message.objects.all().delete()
        self.assertEqual(Message.objects.count(), 0)  # 삭제 후 채팅 기록이 없어야 함

    def test_update_topic(self):
        # 주제 업데이트 테스트
        new_topic = "새로운 주제"
        self.topic.text = new_topic
        self.topic.save()

        updated_topic = Topic.objects.get(id=self.topic.id)
        self.assertEqual(updated_topic.text, new_topic)  # 업데이트된 주제 확인




class CeleryTaskTest(TestCase):
    def test_clear_chat_and_update_topic(self):
        # Celery 작업 호출
        result = clear_chat_and_update_topic.apply()

        # 작업이 성공적으로 실행되었는지 확인
        self.assertTrue(result.successful())
        
        # 작업이 완료된 후 채팅 기록이 삭제되었는지 확인
        self.assertEqual(Message.objects.count(), 0)





class ChatTestCase(TestCase):

    def setUp(self):
        """테스트 전에 필요한 초기 설정"""
        self.redis_stream_name = 'chat_room'

    def test_save_message_to_redis(self):
        """메시지가 Redis에 저장되는지 확인"""
        # Redis에 메시지 추가
        redis_client.xadd(self.redis_stream_name, {'user': 'testuser', 'message': 'Hello Redis'})

        # Redis에서 메시지 가져오기
        messages = redis_client.xrange(self.redis_stream_name)
        self.assertGreater(len(messages), 0)  # 메시지가 하나 이상 있어야 함

        # Redis에서 저장된 메시지 확인
        message_data = messages[-1][1]  # 가장 최근 메시지
        self.assertEqual(message_data['user'], 'testuser')
        self.assertEqual(message_data['message'], 'Hello Redis')

    @patch('chat.task.redis_client.xrange')  # Redis 호출을 mock으로 대체
    def test_save_messages_to_db(self, mock_xrange):
        """Redis에서 DB로 메시지가 저장되는지 확인"""
        # Mock Redis 데이터
        mock_xrange.return_value = [
            ('12345', {'user': 'testuser', 'message': 'Hello DB'})
        ]

        # Celery 작업을 동기적으로 실행하여 DB에 저장
        save_messages_to_db()

        # DB에 저장된 메시지 확인
        message = Message.objects.last()
        self.assertEqual(message.user, 'testuser')
        self.assertEqual(message.content, 'Hello DB')

    def test_celery_task_is_eager(self):
        """Celery가 동기적으로 실행되는지 확인"""
        self.assertEqual(save_messages_to_db(), None)
