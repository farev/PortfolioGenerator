import React from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  height: calc(100vh - 200px);
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  overflow: hidden;
  background: white;
`;

const PreviewFrame = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

const Preview = ({ html }) => {
  // Add default content when no HTML is generated yet
  const defaultContent = `
    <html>
      <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif; color: #666;">
        <div style="text-align: center;">
          <h2>Portfolio Preview</h2>
          <p>Generate your portfolio to see the preview here</p>
        </div>
      </body>
    </html>
  `;

  return (
    <PreviewContainer>
      <PreviewFrame
        srcDoc={html || defaultContent}
        title="Portfolio Preview"
        sandbox="allow-scripts allow-popups"
      />
    </PreviewContainer>
  );
};

export default Preview; 