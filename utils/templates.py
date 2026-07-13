class MessageTemplates:
    """Collection of message templates for different business types"""
    
    TEMPLATES = {
        'restaurant': """
Hi {contact_name},

I've been following {business_name}'s journey and noticed that {pain_point}.

We specialize in helping restaurants optimize their operations and increase customer satisfaction. Our solutions have helped similar establishments reduce costs by 20% and improve customer retention.

Would you be open to a quick chat about how we could help {business_name} achieve similar results?

Best,
[Your Name]
""",
        
        'saas': """
Hi {contact_name},

I've been impressed by {business_name}'s growth in the SaaS space. I noticed you're dealing with {pain_point}.

We help SaaS companies streamline their operations and scale faster. Our solutions have helped companies like yours achieve 30% faster growth and better customer acquisition.

Would you be interested in a brief conversation about this?

Cheers,
[Your Name]
""",
        
        'agency': """
Hi {contact_name},

I've been following {business_name}'s work and saw you're dealing with {pain_point}.

We help marketing agencies scale their operations and deliver better results for their clients. Our framework has helped agencies increase client retention by 40%.

Let me know if you'd be open to exploring this further.

Best,
[Your Name]
""",
        
        'ecommerce': """
Hi {contact_name},

I've been following {business_name}'s growth in the ecommerce space and noticed you're dealing with {pain_point}.

We help ecommerce businesses optimize their operations and increase sales. Our solutions have helped similar stores achieve 25% higher conversion rates.

Would you be open to a brief discussion about how we could help?

Thanks,
[Your Name]
""",
        
        'default': """
Hi {contact_name},

I've been looking at {business_name}'s impressive work in the {business_type} space. I noticed you're dealing with {pain_point}.

We specialize in helping businesses like yours overcome these challenges and achieve better outcomes. Our approach has helped similar companies see significant improvements in their operations.

Would you be open to a short discussion about how we could help?

Thanks,
[Your Name]
"""
    }
    
    @classmethod
    def get_template(cls, business_type: str) -> str:
        """Get template based on business type"""
        business_type = business_type.lower()
        
        # Check if business_type matches any template
        for key in cls.TEMPLATES:
            if key in business_type:
                return cls.TEMPLATES[key]
        
        # Return default template if no match found
        return cls.TEMPLATES['default']
    
    @classmethod
    def get_all_templates(cls) -> dict:
        """Return all available templates"""
        return cls.TEMPLATES
    
    @classmethod
    def get_template_keys(cls) -> list:
        """Return list of available template keys"""
        return list(cls.TEMPLATES.keys())
    # For backward compatibility
MESSAGE_TEMPLATES = MessageTemplates.TEMPLATES