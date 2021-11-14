import React from 'react';
import { Upload, Modal, Card } from 'antd';
import { PlusOutlined } from '@ant-design/icons';


function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

class UploadComponent extends React.Component {

    state = {
        previewVisible: false,
        previewImage: '',
        previewTitle: '',
        // fileList: [],
    };


    handleCancel = () => this.setState({ previewVisible: false });

    handlePreview = async file => {
        if (!file.url && !file.preview) {
            file.preview = await getBase64(file.originFileObj);
        }

        this.setState({
            previewImage: file.url || file.preview,
            previewVisible: true,
            previewTitle: file.name || file.url.substring(file.url.lastIndexOf('/') + 1),
        });
    };

    handleChange = ({ fileList }) => {
        // this.setState({ fileList });
        // let fileObjList = fileList.map((f) => f.originFileObj);
        this.props.handleTargetFileChange(fileList);
    };

    render() {
        const { previewVisible, previewImage, previewTitle } = this.state;
        const uploadButton = (
            <div>
                <PlusOutlined />
                <div style={{ marginTop: 8 }}>Upload</div>
            </div>
        );
        return (
            <>
                <Card title={this.props.cardTitle} >
                    <Upload
                        accept=".jpg, .jpeg, .png"
                        beforeUpload={() => false}
                        listType="picture-card"
                        fileList={this.props.fileList}
                        onPreview={this.handlePreview}
                        onChange={this.handleChange}
                        showUploadList={{ showDownloadIcon: true }}
                    >
                        {this.props.fileList.length >= parseInt(this.props.maxFile) ? null : uploadButton}
                    </Upload>
                </Card>


                <Modal
                    visible={previewVisible}
                    title={previewTitle}
                    footer={null}
                    onCancel={this.handleCancel}
                >
                    <img alt="example" style={{ width: '100%' }} src={previewImage} />
                </Modal>
            </>
        );
    }
}

export default UploadComponent