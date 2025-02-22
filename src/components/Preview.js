import React from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  height: 100%;
  background: #1e1e1e;
`;

const PreviewFrame = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

const Preview = ({ html }) => {
  const defaultContent = `
    <html>
      <head>
        <style>
          body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #1e1e1e;
            color: #d4d4d4;
          }
          .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
          }
          h2 {
            color: #d4d4d4;
            margin-bottom: 1rem;
          }
          p {
            color: #808080;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div>
            <h2>Portfolio Preview</h2>
            <p>Fill in your information and generate to see the preview</p>
          </div>
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