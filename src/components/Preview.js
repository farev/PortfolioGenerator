import React from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  margin: 2rem auto;
  max-width: 1200px;
  padding: 2rem;
`;

const PreviewFrame = styled.iframe`
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
`;

const Preview = ({ html }) => {
  return (
    <PreviewContainer>
      <h2>Generated Portfolio Preview</h2>
      <PreviewFrame
        srcDoc={html}
        title="Portfolio Preview"
        sandbox="allow-scripts"
      />
    </PreviewContainer>
  );
};

export default Preview; 