PORTFOLIO_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Portfolio</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }}

        body {{
            line-height: 1.6;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Header */
        header {{
            padding: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 30px;
        }}

        .nav-links a {{
            text-decoration: none;
            color: #666;
            transition: color 0.3s;
        }}

        .nav-links a:hover {{
            color: #4A90E2;
        }}

        /* Hero Section */
        .hero {{
            padding: 100px 0;
            text-align: center;
            background: white;
        }}

        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: #666;
            margin-bottom: 30px;
        }}

        .cta-button {{
            display: inline-block;
            padding: 12px 30px;
            background: #4A90E2;
            color: white;
            text-decoration: none;
            border-radius: 30px;
            transition: background 0.3s;
        }}

        .cta-button:hover {{
            background: #357ABD;
        }}

        /* About Section */
        .about {{
            padding: 100px 0;
            background: #f8f9fa;
        }}

        .about-content {{
            display: flex;
            align-items: center;
            gap: 50px;
            max-width: 900px;
            margin: 0 auto;
        }}

        .about-image {{
            width: 300px;
            height: 300px;
            border-radius: 50%;
            object-fit: cover;
            background: #ddd;
        }}

        .section-title {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 50px;
        }}

        /* Projects Section */
        .projects {{
            padding: 100px 0;
            background: white;
        }}

        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}

        .project-card {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .project-card:hover {{
            transform: translateY(-5px);
        }}

        .project-image {{
            width: 100%;
            height: 200px;
            background: #ddd;
            object-fit: cover;
        }}

        .project-info {{
            padding: 20px;
        }}

        .project-info h3 {{
            margin-bottom: 10px;
        }}

        .project-info p {{
            color: #666;
            margin-bottom: 15px;
        }}

        .project-link {{
            color: #4A90E2;
            text-decoration: none;
        }}

        .project-link:hover {{
            text-decoration: underline;
        }}

        /* Contact Section */
        .contact {{
            padding: 100px 0;
            background: #f8f9fa;
            text-align: center;
        }}

        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }}

        .social-links a {{
            color: #666;
            font-size: 24px;
            transition: color 0.3s;
        }}

        .social-links a:hover {{
            color: #4A90E2;
        }}

        /* Footer */
        footer {{
            padding: 20px 0;
            text-align: center;
            background: white;
            color: #666;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .about-content {{
                flex-direction: column;
                text-align: center;
            }}

            .hero h1 {{
                font-size: 2.5rem;
            }}

            .about-image {{
                width: 200px;
                height: 200px;
            }}
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
</head>
<body>
    <header>
        <nav class="container">
            <a href="#" class="logo">{name}</a>
            <div class="nav-links">
                <a href="#about">About</a>
                <a href="#projects">Projects</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Welcome to My Portfolio</h1>
            <p>I'm a developer passionate about creating amazing digital experiences</p>
            <a href="#projects" class="cta-button">View My Work</a>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <img src="https://via.placeholder.com/300" alt="Profile" class="about-image">
                <div class="about-text">
                    <p>{about_me}</p>
                    <p>My interests include {interests}</p>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">My Skills</h2>
            <div class="projects-grid">
                {skills_html}
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get in Touch</h2>
            <p>I'm always open to new opportunities and collaborations. Feel free to reach out!</p>
            <div class="social-links">
                <a href="mailto:{email}"><i class="fas fa-envelope"></i></a>
                <a href="{github}"><i class="fab fa-github"></i></a>
                <a href="{linkedin}"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; <script>document.write(new Date().getFullYear())</script> {name}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
'''

def generate_portfolio(user_info):
    # Convert skills string to HTML
    skills_list = [skill.strip() for skill in user_info['skills'].split(',')]
    skills_html = '\n'.join([
        f'''
        <div class="project-card">
            <div class="project-info">
                <h3>{skill}</h3>
            </div>
        </div>
        ''' for skill in skills_list
    ])

    # Replace template variables
    return PORTFOLIO_TEMPLATE.format(
        name=user_info['name'],
        about_me=user_info['about_me'],
        skills_html=skills_html,
        interests=user_info['interests'],
        email=user_info['email'],
        github=user_info['github'],
        linkedin=user_info['linkedin']
    ) 