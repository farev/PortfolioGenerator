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

const LinkedInSection = styled.div`
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #2d2d2d;
  border: 1px solid #404040;
  border-radius: 4px;
`;

const ImportButton = styled.button`
  background-color: #0077b5;
  color: white;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 1rem;
  font-size: 0.9rem;

  &:hover {
    background-color: #006097;
  }

  &:disabled {
    background-color: #2d2d2d;
    cursor: not-allowed;
  }
`;

const GenerateButton = styled.button`
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(90deg,rgb(89, 44, 186),rgb(224, 99, 32)) !important;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;

  &:hover {
    background: linear-gradient(90deg,rgb(9, 9, 120), rgb(158, 69, 21)) !important;
    transform: scale(1.05);

  }

  &:disabled {
    background-color: #2d2d2d;
    cursor: not-allowed;
  }
`;

const DiamondIcon = () => (
  <svg fill="#ffffff" width="12px" height="12px" viewBox="0 0 512 512" id="icons" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M208,512a24.84,24.84,0,0,1-23.34-16l-39.84-103.6a16.06,16.06,0,0,0-9.19-9.19L32,343.34a25,25,0,0,1,0-46.68l103.6-39.84a16.06,16.06,0,0,0,9.19-9.19L184.66,144a25,25,0,0,1,46.68,0l39.84,103.6a16.06,16.06,0,0,0,9.19,9.19l103,39.63A25.49,25.49,0,0,1,400,320.52a24.82,24.82,0,0,1-16,22.82l-103.6,39.84a16.06,16.06,0,0,0-9.19,9.19L231.34,496A24.84,24.84,0,0,1,208,512Zm66.85-254.84h0Z"></path><path d="M88,176a14.67,14.67,0,0,1-13.69-9.4L57.45,122.76a7.28,7.28,0,0,0-4.21-4.21L9.4,101.69a14.67,14.67,0,0,1,0-27.38L53.24,57.45a7.31,7.31,0,0,0,4.21-4.21L74.16,9.79A15,15,0,0,1,86.23.11,14.67,14.67,0,0,1,101.69,9.4l16.86,43.84a7.31,7.31,0,0,0,4.21,4.21L166.6,74.31a14.67,14.67,0,0,1,0,27.38l-43.84,16.86a7.28,7.28,0,0,0-4.21,4.21L101.69,166.6A14.67,14.67,0,0,1,88,176Z"></path><path d="M400,256a16,16,0,0,1-14.93-10.26l-22.84-59.37a8,8,0,0,0-4.6-4.6l-59.37-22.84a16,16,0,0,1,0-29.86l59.37-22.84a8,8,0,0,0,4.6-4.6L384.9,42.68a16.45,16.45,0,0,1,13.17-10.57,16,16,0,0,1,16.86,10.15l22.84,59.37a8,8,0,0,0,4.6,4.6l59.37,22.84a16,16,0,0,1,0,29.86l-59.37,22.84a8,8,0,0,0-4.6,4.6l-22.84,59.37A16,16,0,0,1,400,256Z"></path></g></svg>
  
  
);

//<svg fill="#ffffff" width="8" height="8" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    //<path d="M208,512a24.84,24.84,0,0,1-23.34-16l-39.84-103.6a16.06,16.06,0,0,0-9.19-9.19L32,343.34a25,25,0,0,1,0-46.68l103.6-39.84a16.06,16.06,0,0,0,9.19-9.19L184.66,144a25,25,0,0,1,46.68,0l39.84,103.6a16.06,16.06,0,0,0,9.19,9.19l103,39.63A25.49,25.49,0,0,1,400,320.52a24.82,24.82,0,0,1-16,22.82l-103.6,39.84a16.06,16.06,0,0,0-9.19,9.19L231.34,496A24.84,24.84,0,0,1,208,512Zm66.85-254.84h0Z"></path>
  //s</svg>

const SectionTitle = styled.h2`
  color: #ffffff;
  font-size: 1.1rem;
  margin: 0 0 1.5rem;
  font-weight: normal;
`;

const FileUploadButton = styled.label`
  display: inline-block;
  padding: 0.75rem 1.5rem;
   background: linear-gradient(90deg,rgb(122, 13, 120),rgb(89, 44, 186)) !important;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: center;
  margin-bottom: 1rem;

  &:hover {
    background: linear-gradient(90deg, rgb(122, 13, 120, 0.61),rgb(9, 9, 120)) !important;
  }

  input {
    display: none;
  }
`;

const UserForm = ({ onGenerate, onProjectsUpdate, isGenerating, initialData }) => {
  const [formData, setFormData] = useState(initialData || {
    name: '',
    email: '',
    github: '',
    linkedin: '',
    about_me: '',
    interests: '',
    skills: ''
  });
  const [isImporting, setIsImporting] = useState(false);
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
    try {
      await onGenerate({ ...formData, projects });
      setIsPortfolioGenerated(true);
    } catch (error) {
      console.error('Error generating portfolio:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const importFromLinkedIn = async () => {
    if (!formData.linkedin) {
      alert('Please enter your LinkedIn profile URL');
      return;
    }

    setIsImporting(true);
    try {
      const response = await fetch('http://localhost:8000/parse-linkedin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          profile_url: formData.linkedin 
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to import LinkedIn data');
      }

      const data = await response.json();
      console.log('LinkedIn data:', data); // Debug log

      setFormData(prev => ({
        ...prev,
        name: data.name || prev.name,
        skills: data.skills || prev.skills,
        about_me: data.about_me || prev.about_me,
      }));

      alert('LinkedIn data imported successfully!');

    } catch (error) {
      console.error('Error importing LinkedIn data:', error);
      alert(error.message || 'Failed to import LinkedIn data. Please fill in the information manually.');
    } finally {
      setIsImporting(false);
    }
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
      setFormData(prev => ({
        ...prev,
        ...data
      }));

      alert('Resume parsed successfully!');
    } catch (error) {
      console.error('Error parsing resume:', error);
      alert('Failed to parse resume. Please fill in the information manually.');
    } finally {
      setIsParsingResume(false);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <SectionTitle>Personal Information</SectionTitle>
      
      <FileUploadButton>
        {isParsingResume ? 'Parsing Resume...' : 'Upload Resume'}
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleResumeUpload}
          disabled={isParsingResume}
        />
      </FileUploadButton>

      <LinkedInSection>
        <FormGroup>
          <Label>LinkedIn Profile URL</Label>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Input
              type="url"
              name="linkedin"
              value={formData.linkedin}
              onChange={handleChange}
              placeholder="https://www.linkedin.com/in/your-profile"
            />
            <ImportButton 
              type="button"
              onClick={importFromLinkedIn}
              disabled={isImporting || !formData.linkedin}
            >
              {isImporting ? 'Importing...' : 'Import Data'}
            </ImportButton>
          </div>
        </FormGroup>
      </LinkedInSection>

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
          {isGenerating ? 'Generating...' : (
        <>
          <DiamondIcon /> Generate Portfolio
        </>
      )
          }
        </GenerateButton>
      </div>

      {isPortfolioGenerated && (
        <ProjectForm onProjectsUpdate={handleProjectsUpdate} />
      )}
    </Form>
  );
};

export default UserForm; 