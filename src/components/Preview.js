import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  width: 100%;
  height: 100%;
  overflow: auto;
  background: white;
  position: relative;
`;

const EditableIframe = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

const ImageEditModal = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
  z-index: 1000;
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ImagePreview = styled.div`
  width: 100%;
  height: 200px;
  margin: 10px 0;
  border-radius: 4px;
  overflow: hidden;
  background: #2d2d2d;
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
`;

const FileUploadButton = styled.label`
  display: block;
  width: calc(100% - 32px);
  padding: 8px 16px;
  background: linear-gradient(90deg,rgb(89, 44, 186),rgb(224, 99, 32));
  color: white;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  margin: 10px 0;
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.02);
  }

  input {
    display: none;
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 8px;
  margin: 8px 0;
  background: #2d2d2d;
  border: 1px solid #404040;
  color: white;
  border-radius: 4px;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 15px;
`;

const Button = styled.button`
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: ${props => props.$primary ? '#2ecc71' : '#e74c3c'};
  color: white;
  flex: 1;
  
  &:hover {
    opacity: 0.9;
  }
`;

const Preview = ({ html, onHtmlChange }) => {
  const iframeRef = useRef(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [newImageUrl, setNewImageUrl] = useState('');
  const [previewImage, setPreviewImage] = useState('');

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

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    iframeDoc.open();
    iframeDoc.write(html || defaultContent);
    iframeDoc.close();

    // Only enable design mode if there's actual portfolio content
    if (html) {
      iframeDoc.designMode = 'on';

      const handleImageClick = (e) => {
        if (e.target.tagName === 'IMG') {
          e.preventDefault();
          setSelectedImage(e.target);
          setNewImageUrl(e.target.src);
          setPreviewImage(e.target.src);
          iframeDoc.designMode = 'off';
        }
      };

      const handleChange = () => {
        const updatedHtml = iframeDoc.documentElement.outerHTML;
        onHtmlChange(updatedHtml);
      };

      iframeDoc.addEventListener('click', handleImageClick);
      iframeDoc.addEventListener('input', handleChange);
      iframeDoc.addEventListener('blur', handleChange);

      return () => {
        iframeDoc.removeEventListener('click', handleImageClick);
        iframeDoc.removeEventListener('input', handleChange);
        iframeDoc.removeEventListener('blur', handleChange);
      };
    }
  }, [html, onHtmlChange]);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewImageUrl(reader.result);
        setPreviewImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageUpdate = () => {
    if (selectedImage && newImageUrl) {
      selectedImage.src = newImageUrl;
      const iframeDoc = iframeRef.current.contentDocument;
      onHtmlChange(iframeDoc.documentElement.outerHTML);
    }
    closeImageEditor();
  };

  const closeImageEditor = () => {
    setSelectedImage(null);
    setNewImageUrl('');
    setPreviewImage('');
    const iframeDoc = iframeRef.current.contentDocument;
    iframeDoc.designMode = 'on';
  };

  return (
    <PreviewContainer>
      <EditableIframe ref={iframeRef} title="Portfolio Preview" />
      
      {selectedImage && (
        <ImageEditModal>
          <h3 style={{ color: 'white', marginTop: 0 }}>Edit Image</h3>
          
          <ImagePreview>
            <img src={previewImage || selectedImage.src} alt="Preview" />
          </ImagePreview>

          <FileUploadButton>
            Upload New Image
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
            />
          </FileUploadButton>

          <ButtonGroup>
            <Button $primary onClick={handleImageUpdate}>Update</Button>
            <Button onClick={closeImageEditor}>Cancel</Button>
          </ButtonGroup>
        </ImageEditModal>
      )}
    </PreviewContainer>
  );
};

export default Preview; 