import React, { useState } from 'react';
import ProjectForm from './components/ProjectForm';
import Portfolio from './components/Portfolio';
import Preview from './components/Preview';
import UserForm from './components/UserForm';
import CodeView from './components/CodeView';
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

const SplitLayout = styled.div`
  display: grid;
  grid-template-columns: 45% 55%;
  gap: 2rem;
  margin-top: 2rem;
`;

const LeftPanel = styled.div`
  padding: 1rem;
`;

const RightPanel = styled.div`
  padding: 1rem;
  position: sticky;
  top: 20px;
  height: calc(100vh - 100px);
  overflow-y: auto;
`;

const TabContainer = styled.div`
  display: flex;
  margin-bottom: 1rem;
`;

const Tab = styled.button`
  padding: 0.5rem 1rem;
  background-color: ${props => props.active ? '#007bff' : '#f8f9fa'};
  color: ${props => props.active ? 'white' : '#333'};
  border: 1px solid #dee2e6;
  border-bottom: none;
  cursor: pointer;
  &:first-child {
    border-radius: 4px 0 0 0;
  }
  &:last-child {
    border-radius: 0 4px 0 0;
  }
`;

const GenerateButton = styled.button`
  display: block;
  width: 100%;
  margin: 2rem 0;
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
  const [userInfo, setUserInfo] = useState(null);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeTab, setActiveTab] = useState('preview'); // 'preview' or 'code'

  const handleUserSubmit = (info) => {
    setUserInfo(info);
  };

  const handleProjectSubmit = (project) => {
    setProjects([...projects, project]);
  };

  const handleGenerate = async () => {
    if (!userInfo) {
      alert('Please fill in your personal information first');
      return;
    }

    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/generate-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          user: userInfo,
          projects 
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 429) {
          throw new Error('Rate limit exceeded. Please try again later.');
        }
        throw new Error(errorData.detail || 'Failed to generate portfolio');
      }
      
      const data = await response.json();
      setGeneratedHtml(data.html);
    } catch (error) {
      console.error('Error generating portfolio:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <AppContainer>
      <Header>Portfolio Generator</Header>
      <SplitLayout>
        <LeftPanel>
          <UserForm onSubmit={handleUserSubmit} />
          <ProjectForm onSubmit={handleProjectSubmit} />
          <Portfolio projects={projects} />
          <GenerateButton 
            onClick={handleGenerate}
            disabled={isGenerating || projects.length === 0 || !userInfo}
          >
            {isGenerating ? 'Generating...' : 'Generate Portfolio Page'}
          </GenerateButton>
        </LeftPanel>
        <RightPanel>
          <TabContainer>
            <Tab 
              active={activeTab === 'preview'} 
              onClick={() => setActiveTab('preview')}
            >
              Preview
            </Tab>
            <Tab 
              active={activeTab === 'code'} 
              onClick={() => setActiveTab('code')}
            >
              Code
            </Tab>
          </TabContainer>
          {activeTab === 'preview' ? (
            <Preview html={generatedHtml} />
          ) : (
            <CodeView 
              code={generatedHtml} 
              onChange={setGeneratedHtml}
            />
          )}
        </RightPanel>
      </SplitLayout>
    </AppContainer>
  );
}

export default App; 