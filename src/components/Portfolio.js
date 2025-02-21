import React from 'react';
import styled from 'styled-components';
import ProjectCard from './ProjectCard';

const PortfolioContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

const ProjectsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
`;

const Portfolio = ({ projects }) => {
  return (
    <PortfolioContainer>
      <h1>My Portfolio</h1>
      <ProjectsGrid>
        {projects.map((project, index) => (
          <ProjectCard key={index} project={project} />
        ))}
      </ProjectsGrid>
    </PortfolioContainer>
  );
};

export default Portfolio; 