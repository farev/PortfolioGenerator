def get_portfolio_prompt(user, projects):
    base_prompt = f"""Generate a complete HTML page for a portfolio website. The page should:
1. Use only HTML, CSS (include in a <style> tag), and vanilla JavaScript (include in a <script> tag)
2. Be a single, self-contained file that can be rendered directly in a browser
3. Include all content directly in the HTML (no external imports or frameworks)
4. Use modern CSS features for layout and styling
5. Be responsive and mobile-friendly

Use the following information to create the portfolio:

User Information:
Name: {user.name}
Profession: {user.profession}
Years of Experience: {user.years_experience}
Skills/Expertise: {user.skills}
Interests: {user.interests}
Hobbies: {user.hobbies}
Email: {user.email}
GitHub: {user.github}
LinkedIn: {user.linkedin}
About Me: {user.about_me or ""}

Projects:
"""
    
    for project in projects:
        base_prompt += f"\nTitle: {project.title}\n"
        base_prompt += f"Description: {project.description}\n"
        base_prompt += f"Technologies: {project.technologies}\n"
        if project.image:
            base_prompt += f"Image: {project.image}\n"
        base_prompt += "---"
    
    return base_prompt

SYSTEM_PROMPT = """You are a professional web developer who creates clean, modern portfolio websites. 
Return ONLY the complete HTML document that can be directly rendered in a browser. 
The HTML should include embedded CSS and JavaScript.
Do not include any explanation, only return the HTML code.
The HTML must start with <!DOCTYPE html> and include all necessary tags.
""" 