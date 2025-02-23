import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import ProjectForm from './ProjectForm';

const Form = styled.form`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: #252526;
  border-radius: 8px;
  color: #d4d4d4;
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  color: #cccccc;
  font-size: 0.9rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  background-color: #3c3c3c;
  border: 1px solid #404040;
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.9rem;

  &:focus {
    outline: none;
    border-color: #007acc;
  }

  &::placeholder {
    color: #808080;
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 0.75rem;
  background-color: #3c3c3c;
  border: 1px solid #404040;
  border-radius: 4px;
  color: #ffffff;
  min-height: 100px;
  font-size: 0.9rem;

  &:focus {
    outline: none;
    border-color: #007acc;
  }
`;

const Button = styled.button`
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

const GenerateButton = styled.button`
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;

  &:hover {
    background-color: #45a049;
  }

  &:disabled {
    background-color: #2d2d2d;
    cursor: not-allowed;
  }
`;

const SectionTitle = styled.h2`
  color: #ffffff;
  font-size: 1.1rem;
  margin: 0 0 1.5rem;
  font-weight: normal;
`;

const FileUploadButton = styled.label`
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #2ea043;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: center;
  margin-bottom: 1rem;

  &:hover {
    background-color: #2c974b;
  }

  input {
    display: none;
  }
`;

const ImagePreview = styled.img`
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  margin: 1rem auto;
  display: block;
  background-color: #3c3c3c;
`;

const ImageUploadButton = styled(FileUploadButton)`
  width: 200px;
  margin: 1rem auto;
  display: block;
`;

const fetchGithubProjects = async (githubUrl) => {
  try {
    const response = await fetch('http://localhost:8000/fetch-github-projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ github_url: githubUrl }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch GitHub projects');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching GitHub projects:', error);
    return null;
  }
};

const UserForm = ({ onGenerate, onProjectsUpdate, isGenerating, setIsGenerating, initialData }) => {
  const [formData, setFormData] = useState(initialData || {
    name: '',
    email: '',
    github: '',
    linkedin: '',
    about_me: '',
    interests: '',
    skills: '',
    profileImage: null
  });
  const [isParsingResume, setIsParsingResume] = useState(false);
  const [isPortfolioGenerated, setIsPortfolioGenerated] = useState(false);
  const [projects, setProjects] = useState(initialData?.projects || []);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
      setProjects(initialData.projects || []);
      setIsPortfolioGenerated(true);
    }
  }, [initialData]);

  const handleProjectsUpdate = (updateFn) => {
    const updatedProjects = updateFn(projects);
    setProjects(updatedProjects);
    onProjectsUpdate(updatedProjects);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsGenerating(true);

    try {
      // First, fetch GitHub projects if URL is provided
      let githubProjects = [];
      if (formData.github) {
        const projectsData = await fetchGithubProjects(formData.github);
        if (projectsData && projectsData.projects) {
          githubProjects = projectsData.projects;
        }
      }

      // Add GitHub projects to form data
      const finalFormData = {
        ...formData,
        profileImage: formData.profileImage,
        projects: githubProjects
      };

      await onGenerate(finalFormData);
      setIsPortfolioGenerated(true);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate portfolio');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setIsParsingResume(true);
    try {
      const response = await fetch('http://localhost:8000/parse-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to parse resume');
      }

      const data = await response.json();
      
      // Update form with AI-parsed data
      setFormData(prev => ({
        ...prev,
        skills: data.skills || prev.skills,
        interests: data.interests || prev.interests,
        about_me: data.about_me || prev.about_me,
        linkedin: data.linkedin || prev.linkedin,
        // Keep other fields
        name: data.name || prev.name,
        email: data.email || prev.email,
        github: data.github || prev.github
      }));

      alert('Resume parsed successfully!');
    } catch (error) {
      console.error('Error parsing resume:', error);
      alert('Failed to parse resume. Please fill in the information manually.');
    } finally {
      setIsParsingResume(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData(prev => ({
          ...prev,
          profileImage: reader.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <SectionTitle>Personal Information</SectionTitle>
      
      <FormGroup>
        <Label>Profile Image</Label>
        <ImageUploadButton>
          Upload Profile Picture
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            style={{ display: 'none' }}
          />
        </ImageUploadButton>
        {formData.profileImage && (
          <ImagePreview 
            src={formData.profileImage} 
            alt="Profile preview" 
          />
        )}
      </FormGroup>

      <FileUploadButton>
        {isParsingResume ? 'Parsing Resume...' : 'Upload Resume'}
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleResumeUpload}
          disabled={isParsingResume}
        />
      </FileUploadButton>

      <FormGroup>
        <Label>Name</Label>
        <Input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Skills</Label>
        <TextArea
          name="skills"
          value={formData.skills}
          onChange={handleChange}
          placeholder="e.g., JavaScript, React, Node.js"
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Interests</Label>
        <Input
          type="text"
          name="interests"
          value={formData.interests}
          onChange={handleChange}
          placeholder="e.g., Web Development, AI, Open Source"
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Email</Label>
        <Input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>GitHub URL</Label>
        <Input
          type="url"
          name="github"
          value={formData.github}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>LinkedIn URL</Label>
        <Input
          type="url"
          name="linkedin"
          value={formData.linkedin}
          onChange={handleChange}
        />
      </FormGroup>

      <FormGroup>
        <Label>About Me</Label>
        <TextArea
          name="about_me"
          value={formData.about_me}
          onChange={handleChange}
          placeholder="Tell us about yourself..."
        />
      </FormGroup>

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem' }}>
        <GenerateButton 
          type="submit"
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate Portfolio'}
        </GenerateButton>
      </div>

      {isPortfolioGenerated && (
        <ProjectForm onProjectsUpdate={handleProjectsUpdate} />
      )}
    </Form>
  );
};

export default UserForm; 