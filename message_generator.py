import openai
import pandas as pd
from typing import Dict, Any
import time

class MessageGenerator:
    def __init__(self, api_key: str = None, temperature: float = 0.7):
        if api_key:
            openai.api_key = api_key
        else:
            import os
            openai.api_key = os.getenv("OPENAI_API_KEY")
        
        self.temperature = temperature
        self.model = "gpt-3.5-turbo"  # You can change to gpt-4 if available
    
    def generate_message(self, lead: Dict[str, Any]) -> str:
        """
        Generate a personalized message for a single lead
        """
        business_name = lead.get('business_name', 'Business')
        business_type = lead.get('business_type', 'business')
        pain_point = lead.get('pain_point', 'your challenges')
        contact_name = lead.get('contact_name', '')
        
        # Create prompt
        prompt = f"""Generate a professional WhatsApp outreach message for a business. 

Business Name: {business_name}
Business Type: {business_type}
Pain Point: {pain_point}
Contact Name: {contact_name}

Requirements:
- Personalized greeting (use contact name if provided, else use "Hi there")
- Show understanding of their specific pain point
- Offer a solution or value proposition
- Keep it concise (50-100 words)
- Professional but friendly tone
- Include a clear call to action
- Format as plain text (no emojis, just simple text)

Message:"""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional business development expert who creates personalized outreach messages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=200
            )
            
            message = response.choices[0].message.content.strip()
            return message
            
        except Exception as e:
            # Fallback template if API fails
            return self._generate_template_message(
                business_name, business_type, pain_point, contact_name
            )
    
    def _generate_template_message(self, business_name: str, business_type: str, 
                                   pain_point: str, contact_name: str) -> str:
        """Fallback template message generation"""
        greeting = f"Hi {contact_name}," if contact_name else "Hi there,"
        
        return f"""{greeting}

I hope this message finds you well. I've been following {business_name}'s journey in the {business_type} space and noticed that {pain_point}.

We specialize in helping businesses like yours overcome these exact challenges. Our solutions have helped similar companies achieve significant improvements.

Would you be open to a brief 10-minute chat this week to explore how we might help?

Looking forward to hearing from you!

Best regards,
[Your Name]
[Your Company]"""
    
    def generate_messages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate messages for all leads in the DataFrame
        """
        messages = []
        
        for idx, row in df.iterrows():
            lead = row.to_dict()
            message = self.generate_message(lead)
            messages.append(message)
            
            # Rate limiting to avoid hitting API limits
            time.sleep(0.5)
        
        df['generated_message'] = messages
        return df