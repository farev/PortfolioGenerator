import React, { useState } from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #404040;
`;

const ProjectCard = styled.div`
  background: #2d2d2d;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
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
  background-color: #2ea043;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;

  &:hover {
    background-color: #2c974b;
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

const GenerateButton = styled.button`
  background-color: #0077b5;
  color: white;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
  width: 100%;

  &:hover {
    background-color: #006097;
  }

  &:disabled {
    background-color: #2d2d2d;
    cursor: not-allowed;
  }
`;

const ProjectForm = ({ onProjectsUpdate }) => {
  const [newProject, setNewProject] = useState({
    title: '',
    image: null,
    description: '',
    github: '',
    demo: '',
    live: ''
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

  const generateDescription = async (projectData) => {
    try {
      const response = await fetch('http://localhost:8000/generate-project-description', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: projectData.title,
          image: projectData.image,
          description: projectData.description,
          projectLink: projectData.projectLink
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate description');
      }

      const data = await response.json();
      return data.description;
    } catch (error) {
      console.error('Error generating description:', error);
      return projectData.description;
    }
  };

  const handleAddProject = async (e) => {
    e.preventDefault();
    if (!newProject.title || !newProject.image || !newProject.description) {
      alert('Please provide a title, image, and description');
      return;
    }

    setIsGenerating(true);
    try {
      // Generate enhanced description
      const enhancedDescription = await generateDescription(newProject);
      
      // Create final project with enhanced description
      const finalProject = {
        ...newProject,
        description: enhancedDescription,
      };

      // Update projects list
      onProjectsUpdate(prevProjects => {
        const updatedProjects = [...(prevProjects || []), finalProject];
        return updatedProjects;
      });

      // Reset form
      setNewProject({
        title: '',
        image: null,
        description: '',
        github: '',
        demo: '',
        live: ''
      });

      // Clear file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (error) {
      console.error('Error adding project:', error);
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