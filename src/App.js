import React, { useState } from 'react';
import ProjectForm from './components/ProjectForm';
import Portfolio from './components/Portfolio';
import Preview from './components/Preview';
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

const GenerateButton = styled.button`
  display: block;
  margin: 2rem auto;
  padding: 1rem 2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;

  &:hover {
    background-color: #218838;
  }
`;

function App() {
  const [projects, setProjects] = useState([]);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleProjectSubmit = (project) => {
    setProjects([...projects, project]);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/generate-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ projects }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setGeneratedHtml(data.html);
    } catch (error) {
      console.error('Error generating portfolio:', error);
      // You might want to show an error message to the user here
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <AppContainer>
      <Header>Portfolio Generator</Header>
      <ProjectForm onSubmit={handleProjectSubmit} />
      <Portfolio projects={projects} />
      <GenerateButton 
        onClick={handleGenerate}
        disabled={isGenerating || projects.length === 0}
      >
        {isGenerating ? 'Generating...' : 'Generate Portfolio Page'}
      </GenerateButton>
      {generatedHtml && <Preview html={generatedHtml} />}
    </AppContainer>
  );
}

export default App; 