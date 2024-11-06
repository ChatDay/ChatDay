from django.test import TestCase
from .models import Topic,Message
from chat.task import clear_chat_and_update_topic
from celery.result import AsyncResult

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