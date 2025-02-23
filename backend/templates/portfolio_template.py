PORTFOLIO_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Portfolio</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{
            --primary-color: #007acc;
            --text-color: #333;
            --bg-color: #fff;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            color: var(--text-color);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Header */
        header {{
            padding: 20px 0;
            background: white;
        }}

        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #000;
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 30px;
        }}

        .nav-links a {{
            text-decoration: none;
            color: #666;
            font-size: 1rem;
            transition: color 0.3s;
        }}

        .nav-links a:hover {{
            color: #000;
        }}

        /* Hero Section */
        .hero {{
            padding: 120px 0;
            text-align: center;
            background: white;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 20px;
            color: #000;
            font-weight: bold;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: #666;
            margin-bottom: 40px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}

        .cta-button {{
            display: inline-flex;
            align-items: center;
            padding: 15px 30px;
            background: #1a73e8;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-size: 1rem;
            transition: background 0.3s;
        }}

        .cta-button:hover {{
            background: #1557b0;
        }}

        .cta-button::after {{
            content: "→";
            margin-left: 8px;
            font-size: 1.2rem;
        }}

        /* About Section */
        .about {{
            padding: 100px 0;
            background: #f8f9fa;
        }}

        .about-section {{
            padding: 100px 0;
            background: #f8f9fa;
        }}

        .about-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            max-width: 1000px;
            margin: 0 auto;
        }}

        .about-image {{
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: #f0f0f0;
        }}

        .about-text {{
            font-size: 1.1rem;
            color: #333;
        }}

        .about-text p {{
            margin-bottom: 20px;
        }}

        /* Skills Section */
        .skills {{
            padding: 100px 0;
            background: white;
        }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}

        .skill-card {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .skill-card:hover {{
            transform: translateY(-5px);
        }}

        .skill-info {{
            padding: 20px;
        }}

        .skill-info h3 {{
            margin-bottom: 10px;
        }}

        .skill-info p {{
            color: #666;
            margin-bottom: 15px;
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
            .hero h1 {{
                font-size: 2.5rem;
            }}

            .about-content {{
                grid-template-columns: 1fr;
                text-align: center;
            }}

            .about-image {{
                width: 300px;
                height: 300px;
                margin: 0 auto;
            }}
        }}

        /* Project Links */
        .project-links {{
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }}

        .project-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background-color: #2d2d2d;
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: background-color 0.2s;
        }}

        .project-link:hover {{
            background-color: #404040;
        }}

        .project-link i {{
            font-size: 1rem;
        }}
    </style>
</head>
<body>
    <header>
        <nav class="container">
            <a href="#" class="logo">{name}</a>
            <div class="nav-links">
                <a href="#about">About</a>
                <a href="#skills">Skills</a>
                <a href="#projects">Projects</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{name}</h1>
            <a href="#projects" class="cta-button">View My Work</a>
        </div>
    </section>

    <div class="about-section">
        <div class="container">
            <div class="about-content">
                <div class="about-image" style="width: 400px; height: 400px; border-radius: 50%; overflow: hidden;">
                    {profile_image}
                </div>
                <div class="about-text">
                    <p>{about_me}</p>
                </div>
            </div>
        </div>
    </div>

    <section id="skills" class="skills">
        <div class="container">
            <h2 class="section-title">Skills</h2>
            <div class="skills-grid">
                {skills_html}
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Projects</h2>
            <div class="projects-grid">
                {projects_html}
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get in Touch</h2>
            <p>I'm always open to new opportunities and collaborations.</p>
            <div class="social-links">
                <a href="mailto:{email}"><i class="fas fa-envelope"></i></a>
                <a href="{github}"><i class="fab fa-github"></i></a>
                <a href="{linkedin}"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; {name} 2024. All rights reserved.</p>
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
        <div class="skill-card">
            <div class="skill-info">
                <h3>{skill}</h3>
            </div>
        </div>
        ''' for skill in skills_list
    ])

    # Generate projects HTML
    projects = user_info.get('projects', [])
    if not projects:
        projects_html = '''
        <div class="empty-projects">
            <p>No projects added yet.</p>
        </div>
        '''
    else:
        projects_html = '\n'.join([
            f'''
            <div class="project-card">
                <div class="project-image-container">
                    <img src="{project['image']}" alt="{project['title']}" class="project-image">
                </div>
                <div class="project-info">
                    <h3>{project['title']}</h3>
                    <p class="project-description">{project['description']}</p>
                    {f'<p class="project-technologies">Technologies: {project["technologies"]}</p>' if project.get("technologies") else ''}
                    <div class="project-links">
                        {f'<a href="{project["github"]}" class="project-link" target="_blank"><i class="fab fa-github"></i> GitHub</a>' if project.get('github') else ''}
                        {f'<a href="{project["live"]}" class="project-link" target="_blank"><i class="fas fa-external-link-alt"></i> Live</a>' if project.get('live') else ''}
                    </div>
                </div>
            </div>
            ''' for project in projects
        ])

    # Create the profile image HTML
    profile_image_html = ''
    if user_info.get('profileImage'):
        profile_image_html = f'<img src="{user_info["profileImage"]}" alt="Profile" style="width: 100%; height: 100%; object-fit: cover;">'
    
    # Return the formatted template
    return PORTFOLIO_TEMPLATE.format(
        name=user_info['name'],
        about_me=user_info.get('about_me', f"Hello! I'm {user_info['name']}. I specialize in {user_info.get('skills', '')} and I'm passionate about {user_info.get('interests', '')}."),
        skills_html=skills_html,
        projects_html=projects_html,
        email=user_info['email'],
        github=user_info['github'],
        linkedin=user_info.get('linkedin', '#'),
        profile_image=profile_image_html
    )