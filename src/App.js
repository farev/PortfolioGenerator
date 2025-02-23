import React, { useState } from 'react';
import styled from 'styled-components';
import CodeView from './components/CodeView';
import Preview from './components/Preview';
import UserForm from './components/UserForm';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #1e1e1e;
  color: #fff;
`;

//background-color: #2d2d2d
//border-bottom: 1px solid #404040;
const Header = styled.div`
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #1C1A1E; 
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 400px 1fr;
  height: calc(100vh - 48px); // Adjust based on header height
`;

//background-color: #252526;
//border-right: 1px solid #404040;
const Sidebar = styled.div`
  background-color: #1E1E1E;
  
  overflow-y: auto;
  padding: 1rem;
`;

const EditorSection = styled.div`
  display: flex;
  flex-direction: column;
`;

const TabBar = styled.div`
  display: flex;
  background-color: #1e1e1e;
  padding: 0.5rem;
  gap: 0.5rem;
`;

const Tab = styled.button`
  background-color: ${props => props.$active ? '#262626' : 'transparent'};
  color: ${props => props.$active ? '#fff' : '#999'};
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: ${props => props.$active ? '#1e1e1e' : '#333'};
  }
`;

const EditorContainer = styled.div`
  flex: 1;
  overflow: hidden;
`;

//background-color: linear-gradient #7218AA, #B620E0);
const DeployButton = styled.button`
  background: linear-gradient(90deg,rgb(89, 44, 186),rgb(224, 99, 32)) !important;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  margin-left: auto;
  cursor: pointer;
  &:hover {
    background: linear-gradient(90deg,rgb(9, 9, 120), rgb(158, 69, 21)) !important;
    transform: scale(1.05);

  }
`;



function App() {
  const [userInfo, setUserInfo] = useState(null);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [activeTab, setActiveTab] = useState('preview');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (formData) => {
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/generate-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate portfolio');
      }

      const data = await response.json();
      setGeneratedHtml(data.html);
      setUserInfo(formData);
      setActiveTab('preview');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate portfolio');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleProjectsUpdate = async (projects) => {
    if (!userInfo) return;

    try {
      const updatedUserInfo = {
        ...userInfo,
        projects
      };

      const response = await fetch('http://localhost:8000/generate-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedUserInfo),
      });

      if (!response.ok) {
        throw new Error('Failed to update portfolio');
      }

      const data = await response.json();
      setGeneratedHtml(data.html);
      setUserInfo(updatedUserInfo);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to update portfolio with new project');
    }
  };

  const handleDeploy = async () => {
    // Implement deployment logic here
    alert('Deployment feature coming soon!');
  };
  
// change Folio size
  return (
    <AppContainer>
      <Header>
        <h1 style={{ fontSize: '1.2rem', margin: 0 }}><img src="FolioAILogo.png" alt="FolioAI" width={120}/></h1>
        <DeployButton onClick={handleDeploy}>Deploy</DeployButton>
      </Header>
      <MainContent>
        <Sidebar>
          <UserForm 
            onGenerate={handleGenerate}
            onProjectsUpdate={handleProjectsUpdate}
            isGenerating={isGenerating}
            setIsGenerating={setIsGenerating}
            initialData={userInfo}
          />
        </Sidebar>
        <EditorSection>
          <TabBar>
            <Tab 
              $active={activeTab === 'preview'}
              onClick={() => setActiveTab('preview')}
            >
              Preview
            </Tab>
            <Tab 
              $active={activeTab === 'code'}
              onClick={() => setActiveTab('code')}
            >
              Code
            </Tab>
          </TabBar>
          <EditorContainer>
            {activeTab === 'preview' ? (
              <Preview html={generatedHtml} />
            ) : (
              <CodeView 
                code={generatedHtml} 
                onChange={setGeneratedHtml}
              />
            )}
          </EditorContainer>
        </EditorSection>
      </MainContent>
    </AppContainer>
  );
}

export default App; 