import React from 'react';
import styled from 'styled-components';
import Editor from '@monaco-editor/react';

const CodeViewContainer = styled.div`
  height: calc(100vh - 200px);
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  overflow: hidden;
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
        theme="vs-light"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          wordWrap: 'on',
          lineNumbers: 'on',
          folding: true,
          formatOnPaste: true,
          formatOnType: true,
          autoIndent: 'full',
          lineDecorationsWidth: 0,
          lineNumbersMinChars: 3,
        }}
      />
    </CodeViewContainer>
  );
};

export default CodeView; 