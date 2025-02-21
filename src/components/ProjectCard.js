import React from 'react';
import styled from 'styled-components';

const Card = styled.div`
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  margin: 1rem;
  background: white;
`;

const Image = styled.img`
  width: 100%;
  height: 200px;
  object-fit: cover;
`;

const Content = styled.div`
  padding: 1rem;
`;

const Title = styled.h3`
  margin: 0 0 0.5rem 0;
`;

const Description = styled.p`
  color: #666;
`;

const Technologies = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const Tech = styled.span`
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
`;

const ProjectCard = ({ project }) => {
  return (
    <Card>
      {project.image && <Image src={project.image} alt={project.title} />}
      <Content>
        <Title>{project.title}</Title>
        <Description>{project.description}</Description>
        <Technologies>
          {project.technologies.split(',').map((tech, index) => (
            <Tech key={index}>{tech.trim()}</Tech>
          ))}
        </Technologies>
      </Content>
    </Card>
  );
};

export default ProjectCard; 