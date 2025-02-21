import React, { useState } from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Input = styled.input`
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const TextArea = styled.textarea`
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 100px;
`;

const Button = styled.button`
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

const ProjectForm = ({ onSubmit }) => {
  const [project, setProject] = useState({
    title: '',
    description: '',
    image: null,
    technologies: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(project);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProject({ ...project, image: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <FormContainer>
      <Form onSubmit={handleSubmit}>
        <h2>Add New Project</h2>
        <Input
          type="text"
          placeholder="Project Title"
          value={project.title}
          onChange={(e) => setProject({ ...project, title: e.target.value })}
        />
        <TextArea
          placeholder="Project Description"
          value={project.description}
          onChange={(e) => setProject({ ...project, description: e.target.value })}
        />
        <Input
          type="text"
          placeholder="Technologies Used (comma-separated)"
          value={project.technologies}
          onChange={(e) => setProject({ ...project, technologies: e.target.value })}
        />
        <Input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
        />
        <Button type="submit">Add Project</Button>
      </Form>
    </FormContainer>
  );
};

export default ProjectForm; 