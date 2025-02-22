import React, { useState } from 'react';
import styled from 'styled-components';

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

const UserForm = ({ onSubmit, onGenerate, isGenerating }) => {
  const [userInfo, setUserInfo] = useState({
    name: '',
    skills: '',
    interests: '',
    email: '',
    github: '',
    linkedin: '',
    about_me: ''
  });

  const [isImporting, setIsImporting] = useState(false);
  const [isParsingResume, setIsParsingResume] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(userInfo);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const importFromLinkedIn = async () => {
    if (!userInfo.linkedin) {
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
          profile_url: userInfo.linkedin 
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to import LinkedIn data');
      }

      const data = await response.json();
      console.log('LinkedIn data:', data); // Debug log

      setUserInfo(prev => ({
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
      setUserInfo(prev => ({
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
              value={userInfo.linkedin}
              onChange={handleChange}
              placeholder="https://www.linkedin.com/in/your-profile"
            />
            <ImportButton 
              type="button"
              onClick={importFromLinkedIn}
              disabled={isImporting || !userInfo.linkedin}
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
          value={userInfo.name}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Skills</Label>
        <TextArea
          name="skills"
          value={userInfo.skills}
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
          value={userInfo.interests}
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
          value={userInfo.email}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>GitHub URL</Label>
        <Input
          type="url"
          name="github"
          value={userInfo.github}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>About Me</Label>
        <TextArea
          name="about_me"
          value={userInfo.about_me}
          onChange={handleChange}
          placeholder="Tell us about yourself..."
        />
      </FormGroup>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
        <Button type="submit">Save Information</Button>
        <GenerateButton 
          type="button"
          onClick={onGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate Portfolio'}
        </GenerateButton>
      </div>
    </Form>
  );
};

export default UserForm; 