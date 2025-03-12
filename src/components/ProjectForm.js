import React, { useState } from 'react';
import styled from 'styled-components';
import config from '../config';

const FormContainer = styled.div`
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #404040;
`;

const ImagePreview = styled.img`
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 1rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  background-color: #3c3c3c;
  border: 1px solid #404040;
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.9rem;
  margin-bottom: 1rem;

  &:focus {
    outline: none;
    border-color: #007acc;
  }
`;

const AddButton = styled.button`
  width: 200px;
  margin: 1rem auto;
  display: block;
  padding: 0.75rem;
  background: linear-gradient(90deg,rgb(122, 13, 120),rgb(89, 44, 186)) !important;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background: linear-gradient(90deg, rgb(122, 13, 120, 0.61),rgb(9, 9, 120)) !important;
    transform: scale(1.05);
  }

  &:disabled {
    background-color: #2d2d2d;
    cursor: not-allowed;
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
  margin-bottom: 1rem;

  &:focus {
    outline: none;
    border-color: #007acc;
  }
`;

const ProjectForm = ({ onProjectsUpdate }) => {
  const [newProject, setNewProject] = useState({
    title: '',
    image: null,
    description: '',
    github: '',
    demo: '',
    live: '',
    technologies: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewProject(prev => ({
          ...prev,
          image: reader.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProject(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAddProject = async (e) => {
    e.preventDefault();
    if (!newProject.title || !newProject.description) {
      alert('Please provide at least a title and description');
      return;
    }

    setIsGenerating(true);
    try {
      // Generate enhanced description using the correct endpoint
      const response = await fetch(`${config.apiBaseUrl}/generate-project-description`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newProject.title,
          image: newProject.image,
          description: newProject.description,
          projectLink: newProject.github || newProject.live || ''
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to enhance description');
      }

      const data = await response.json();
      const enhancedDescription = data.description || newProject.description;

      // Create final project with enhanced description
      const finalProject = {
        title: newProject.title,
        description: enhancedDescription,
        image: newProject.image || '',
        github: newProject.github || '',
        demo: newProject.demo || '',
        live: newProject.live || '',
        technologies: newProject.technologies || ''
      };

      // Update projects list
      onProjectsUpdate(currentProjects => [...(currentProjects || []), finalProject]);

      // Reset form
      setNewProject({
        title: '',
        image: null,
        description: '',
        github: '',
        demo: '',
        live: '',
        technologies: ''
      });

      // Clear file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (error) {
      console.error('Error adding project:', error);
      alert(`Failed to add project: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <FormContainer>
      <h2>Add Project</h2>
      <div>
        <Input
          type="text"
          name="title"
          value={newProject.title}
          onChange={handleInputChange}
          placeholder="Project Title"
          required
        />
        
        <Input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          required
        />

        {newProject.image && (
          <ImagePreview src={newProject.image} alt="Project preview" />
        )}

        <TextArea
          name="description"
          value={newProject.description}
          onChange={handleInputChange}
          placeholder="Project Description"
          required
        />

        <Input
          type="url"
          name="github"
          value={newProject.github}
          onChange={handleInputChange}
          placeholder="GitHub Repository URL (Optional)"
        />

        <Input
          type="url"
          name="demo"
          value={newProject.demo}
          onChange={handleInputChange}
          placeholder="Demo Video URL (Optional)"
        />

        <Input
          type="url"
          name="live"
          value={newProject.live}
          onChange={handleInputChange}
          placeholder="Live Project URL (Optional)"
        />

        <Input
          type="text"
          name="technologies"
          value={newProject.technologies}
          onChange={handleInputChange}
          placeholder="Technologies Used (comma-separated)"
        />

        <AddButton 
          onClick={handleAddProject}
          disabled={isGenerating}
        >
          {isGenerating ? 'Enhancing Description...' : 'Add Project'}
        </AddButton>
      </div>
    </FormContainer>
  );
};

export default ProjectForm; 