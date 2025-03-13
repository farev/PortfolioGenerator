import React, { useState } from 'react';
import styled from 'styled-components';
import CodeView from './components/CodeView';
import Preview from './components/Preview';
import UserForm from './components/UserForm';
import config from './config';

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

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
  gap: 1rem;
`;

const DeployedUrlContainer = styled.div`
  background: #2d2d2d;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;

  p {
    margin: 0 0 0.5rem;
    color: #ffffff;
  }

  a {
    color: #2ecc71;
    text-decoration: none;
    word-break: break-all;

    &:hover {
      text-decoration: underline;
    }
  }
`;

function App() {
  const [userInfo, setUserInfo] = useState(null);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [activeTab, setActiveTab] = useState('preview');
  const [isGenerating, setIsGenerating] = useState(false);
  const [deployedUrl, setDeployedUrl] = useState(null);
  const [portfolioHtml, setPortfolioHtml] = useState('');
  const [generatedPortfolio, setGeneratedPortfolio] = useState(null);
  const [portfolioUrl, setPortfolioUrl] = useState('');

  const handleGenerate = async (userData) => {
    try {
      setIsGenerating(true);
      
      // If userData already has html_content, use it directly
      if (userData.html_content) {
        setPortfolioHtml(userData.html_content);
        setGeneratedPortfolio(userData);
        setActiveTab('preview');
        setIsGenerating(false);
        return;
      }
      
      // Make API call to generate portfolio
      const response = await fetch(`${config.apiBaseUrl}/generate-portfolio`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate portfolio');
      }
      
      const data = await response.json();
      
      // Make sure we're capturing the HTML content from the response
      setPortfolioHtml(data.html_content);
      
      // Store the portfolio data
      setGeneratedPortfolio({
        ...userData,
        slug: data.slug
      });
      
      // Set the portfolio URL
      setPortfolioUrl(`/${data.slug}`);
      
      // Switch to preview tab automatically
      setActiveTab('preview');
      
    } catch (error) {
      console.error('Error generating portfolio:', error);
      alert('Failed to generate portfolio');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleProjectsUpdate = async (updatedProjects) => {
    try {
      if (!generatedPortfolio || !generatedPortfolio.slug) {
        throw new Error('No portfolio data available');
      }

      // Get the new project (last item in updatedProjects array)
      const newProject = updatedProjects[updatedProjects.length - 1];
      
      // Make API call to add-project endpoint with complete portfolio data
      const response = await fetch(`${config.apiBaseUrl}/add-project/${generatedPortfolio.slug}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...newProject,
          name: generatedPortfolio.name,
          email: generatedPortfolio.email,
          github: generatedPortfolio.github,
          linkedin: generatedPortfolio.linkedin,
          about_me: generatedPortfolio.about_me,
          skills: generatedPortfolio.skills,
          interests: generatedPortfolio.interests,
          profile_image: generatedPortfolio.profile_image,
          html_content: portfolioHtml
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update portfolio');
      }

      // Update local state with new data
      setGeneratedPortfolio(prevPortfolio => ({
        ...prevPortfolio,
        projects: updatedProjects
      }));
      
      // Fetch the updated portfolio HTML
      const portfolioResponse = await fetch(`${config.apiBaseUrl}/portfolio/${generatedPortfolio.slug}`);
      if (!portfolioResponse.ok) {
        throw new Error('Failed to fetch updated portfolio');
      }
      
      const html = await portfolioResponse.text();
      setPortfolioHtml(html);

    } catch (error) {
      console.error('Error updating portfolio:', error);
      alert(`Failed to update portfolio: ${error.message}`);
    }
  };

  const handleDeploy = async () => {
    try {
      // Check if we have either userInfo or generatedPortfolio
      if (!userInfo && !generatedPortfolio) {
        alert('Please generate a portfolio first!');
        return;
      }

      // Use generatedPortfolio if available, otherwise fall back to userInfo
      const portfolioData = generatedPortfolio || userInfo;
      
      const response = await fetch(`${config.apiBaseUrl}/deploy-portfolio`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...portfolioData,
          base_url: window.location.origin,
          html_content: portfolioHtml || generatedHtml
        })
      });

      if (!response.ok) {
        throw new Error('Failed to deploy portfolio');
      }

      const data = await response.json();
      const fullUrl = `${config.apiBaseUrl}/portfolio${data.url}`;
      setDeployedUrl(fullUrl);
      
      // Open the deployed portfolio in a new tab
      window.open(fullUrl, '_blank');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to deploy portfolio');
    }
  };

  const handleHtmlChange = (newHtml) => {
    setPortfolioHtml(newHtml);
  };

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
            initialData={generatedPortfolio}
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
              <>
                <Preview 
                  html={portfolioHtml} 
                  onHtmlChange={handleHtmlChange} 
                />
                <ButtonContainer>
                  <DeployButton 
                    onClick={handleDeploy}
                    disabled={!portfolioHtml}
                  >
                    Deploy Portfolio
                  </DeployButton>
                  {deployedUrl && (
                    <DeployedUrlContainer>
                      <p>Your portfolio is live at:</p>
                      <a href={deployedUrl} target="_blank" rel="noopener noreferrer">
                        {deployedUrl}
                      </a>
                    </DeployedUrlContainer>
                  )}
                </ButtonContainer>
              </>
            ) : (
              <CodeView 
                code={portfolioHtml} 
                onChange={handleHtmlChange}
              />
            )}
          </EditorContainer>
        </EditorSection>
      </MainContent>
    </AppContainer>
  );
}

export default App; 