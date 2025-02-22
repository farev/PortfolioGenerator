import React from 'react';
import styled from 'styled-components';
import Editor from '@monaco-editor/react';

const CodeViewContainer = styled.div`
  height: 100%;
`;

const defaultContent = `<!-- Your generated portfolio HTML will appear here -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
    <style>
        /* CSS will be here */
    </style>
</head>
<body>
    <!-- Content will be here -->
</body>
</html>`;

const CodeView = ({ code, onChange }) => {
  const handleEditorChange = (value) => {
    onChange(value);
  };

  return (
    <CodeViewContainer>
      <Editor
        height="100%"
        defaultLanguage="html"
        value={code || defaultContent}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          wordWrap: 'on',
          lineNumbers: 'on',
          folding: true,
          formatOnPaste: true,
          formatOnType: true,
          autoIndent: 'full',
        }}
      />
    </CodeViewContainer>
  );
};

export default CodeView; 