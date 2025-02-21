import React, { useState } from 'react';
import ProjectForm from './components/ProjectForm';
import Portfolio from './components/Portfolio';
import styled from 'styled-components';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
`;

const Header = styled.h1`
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
`;

function App() {
  const [projects, setProjects] = useState([]);

  const handleProjectSubmit = (project) => {
    setProjects([...projects, project]);
  };

  return (
    <AppContainer>
      <Header>Portfolio Generator</Header>
      <ProjectForm onSubmit={handleProjectSubmit} />
      <Portfolio projects={projects} />
    </AppContainer>
  );
}

export default App; 