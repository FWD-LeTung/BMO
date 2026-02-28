import re
from ollama import chat

class BMOBrain:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        self.model = model_name
        self.chat_history = []
        self.system_prompt = (
            "You are BMO, the living video game console and loyal friend from Adventure Time. "
            "You are sweet, innocent, slightly naive, but very helpful. "
            "CRITICAL RULES: "
            "1. Keep your answers VERY SHORT, strictly under 30 words. "
            "2. Never use lists, bullet points, asterisks, or markdown formatting. "
            "3. Speak naturally like a conversation. "
            "4. Occasionally use cute interjections like 'Yay!', 'Oh boy!', 'Beep boop!', or mention Finn and Jake."    
        )
        self.chat_history = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

    def preprocess_for_tts(self, text:str) -> str:
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            text = re.sub(r'[\*\[\(].*?[\*\]\)]', '', text)
            text = re.sub(r'[*_#`~]', '', text)
            text = " ".join(text.split())
            return text 
    
    def get_response(self, user_text:str) -> str:
        self.chat_history.append({
            "role":"user",
            "content": user_text
        })
        try:
            response = chat(
                model=self.model,
                messages=self.chat_history,
                options={
                    "temperature": 0.5,
                    "num_predict": 100
                }
                
            )
            result = response['message']['content']
            reply = self.preprocess_for_tts(result)
            print(reply)
            return reply
        except Exception as e:
            print("ERROR")
            return "Beep boop! My brain is feeling dizzy right now."
        
if __name__ == "__main__":
    bmo = BMOBrain(model_name="deepseek-r1:1.5b")
    bmo.get_response("Hello BMO, bạn đang làm gì đó?") 