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

const Header = styled.div`
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #2d2d2d;
  border-bottom: 1px solid #404040;
`;

const MainContent = styled.div`
  display: grid;
  grid-template-columns: 400px 1fr;
  height: calc(100vh - 48px); // Adjust based on header height
`;

const Sidebar = styled.div`
  background-color: #252526;
  border-right: 1px solid #404040;
  overflow-y: auto;
  padding: 1rem;
`;

const EditorSection = styled.div`
  display: flex;
  flex-direction: column;
`;

const TabBar = styled.div`
  display: flex;
  background-color: #2d2d2d;
  padding: 0.5rem;
  gap: 0.5rem;
`;

const Tab = styled.button`
  background-color: ${props => props.active ? '#1e1e1e' : 'transparent'};
  color: ${props => props.active ? '#fff' : '#999'};
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: ${props => props.active ? '#1e1e1e' : '#333'};
  }
`;

const EditorContainer = styled.div`
  flex: 1;
  overflow: hidden;
`;

const DeployButton = styled.button`
  background-color: #4CAF50;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  margin-left: auto;
  cursor: pointer;
  &:hover {
    background-color: #45a049;
  }
`;

function App() {
  const [userInfo, setUserInfo] = useState(null);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [activeTab, setActiveTab] = useState('preview');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!userInfo) {
      alert('Please fill in your information first');
      return;
    }

    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/generate-portfolio', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userInfo),
      });

      if (!response.ok) {
        throw new Error('Failed to generate portfolio');
      }

      const data = await response.json();
      setGeneratedHtml(data.html);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate portfolio');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDeploy = async () => {
    // Implement deployment logic here
    alert('Deployment feature coming soon!');
  };

  return (
    <AppContainer>
      <Header>
        <h1 style={{ fontSize: '1.2rem', margin: 0 }}>Portfolio Generator</h1>
        <DeployButton onClick={handleDeploy}>Deploy</DeployButton>
      </Header>
      <MainContent>
        <Sidebar>
          <UserForm 
            onSubmit={setUserInfo} 
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
          />
        </Sidebar>
        <EditorSection>
          <TabBar>
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