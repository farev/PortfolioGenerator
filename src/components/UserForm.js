import React, { useState } from 'react';
import styled from 'styled-components';

const Form = styled.form`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 100px;
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
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const ImportButton = styled.button`
  background-color: #0077b5;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 1rem;

  &:hover {
    background-color: #006097;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const UserForm = ({ onSubmit }) => {
  const [userInfo, setUserInfo] = useState({
    name: '',
    profession: '',
    years_experience: '',
    skills: '',
    interests: '',
    hobbies: '',
    email: '',
    github: '',
    linkedin: '',
    about_me: ''
  });

  const [isImporting, setIsImporting] = useState(false);

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
        profession: data.profession || prev.profession,
        years_experience: data.years_experience || prev.years_experience,
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

  return (
    <Form onSubmit={handleSubmit}>
      <h2>Personal Information</h2>
      
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
        <Label>Profession</Label>
        <Input
          type="text"
          name="profession"
          value={userInfo.profession}
          onChange={handleChange}
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Years of Experience</Label>
        <Input
          type="number"
          name="years_experience"
          value={userInfo.years_experience}
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
          required
        />
      </FormGroup>

      <FormGroup>
        <Label>Hobbies</Label>
        <Input
          type="text"
          name="hobbies"
          value={userInfo.hobbies}
          onChange={handleChange}
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
        />
      </FormGroup>

      <Button type="submit">Save Information</Button>
    </Form>
  );
};

export default UserForm; 