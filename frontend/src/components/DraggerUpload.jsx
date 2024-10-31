import React from "react";
import { InboxOutlined } from "@ant-design/icons";
import { Upload } from "antd";
import FormControl from "@mui/material/FormControl";

const DraggerUpload = ({ fileList, setFileList, primaryColor }) => {
  //config arquivos suportados
  const SUPPORTED_FILE_TYPES = [
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/heic",
  ];
  const { Dragger } = Upload;

  return (
    <FormControl fullWidth>
      <Dragger
        beforeUpload={(file) => {
          if (SUPPORTED_FILE_TYPES.some((x) => x === file.type)) {
            setFileList([...fileList, file]);
            return false;
          }

          return Upload.LIST_IGNORE;
        }}
        fileList={fileList}
        maxCount={5}
        multiple
        onChange={(info) => {
          let newFileList = [...info.fileList];
          newFileList = newFileList.slice(-4);
          setFileList(newFileList);
        }}
        onRemove={(file) => {
          const index = fileList.indexOf(file);
          const newFileList = fileList.slice();
          newFileList.splice(index, 1);
          setFileList(newFileList);
        }}
      >
        <p className="ant-upload-drag-icon">
          <InboxOutlined style={{ color: primaryColor }} />
        </p>
        <p className="ant-upload-text">
          Clique ou arraste o arquivo para esta área para fazer upload
        </p>
        <p className="ant-upload-hint">
          Suporte para upload único ou em massa. Estritamente proibido de fazer
          upload de dados de empresas ou outros arquivos proibidos.
        </p>
        <p className="ant-upload-hint">
          Arquivos suportados: {SUPPORTED_FILE_TYPES.join(", ")}
        </p>
      </Dragger>
    </FormControl>
  );
};

export default DraggerUpload;
