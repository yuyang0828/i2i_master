import React from 'react';
import './App.css';

import UploadComponent from './components/uploadComponent';
import TranslateBtn from './components/translateBtn';
import ShowResult from './components/showResult';
import { Button, Layout } from 'antd';

const { Header, Content, Footer } = Layout;


class App extends React.Component {
  state = {
    targetFileList: [],
    sourceFileList: [],
    resultFileList: [],
    mode: 'cnn'
  };

  handleTargetFileChange = (fileList) => {
    // let fileObjList = fileList.map((f) => f.originFileObj);
    // console.log(fileObjList);
    this.setState({ targetFileList: fileList })
  }

  handleResultFileChange = (fileList) => {
    // let fileObjList = fileList.map((f) => f.originFileObj);
    // console.log(fileObjList);
    this.setState({ sourceFileList: fileList })
  }

  getResultFileList = (fileList) => {
    console.log(fileList)
    this.setState({ resultFileList: fileList })
  }

  cnn = () => {
    this.setState({ mode: 'cnn' })
    this.setState({ targetFileList: [] })
    this.setState({ sourceFileList: [] })
    this.setState({ resultFileList: [] })
  }

  gan = () => {
    this.setState({ mode: 'gan' })
    this.setState({ resultFileList: [] })
    this.setState({ targetFileList: [] })
    this.setState({ sourceFileList: [] })

  }

  render() {
    return (
      <Layout className="layout">
        <Header>
          <div className="title">I2I MASTER</div>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <div className="site-layout-content">

            <div style={{ marginBottom: '24px' }}>

              <Button type="primary" shape="round" onClick={this.cnn} style={{ marginRight: '24px' }}>CNN + TPS + FUSION</Button>
              <Button type="primary" shape="round" onClick={this.gan}>GAN</Button>

            </div>

            <div style={{ display: 'flex' }}>
              {this.state.mode == 'cnn' ?
                <>
                  <div style={{ marginRight: '48px' }} >
                    <UploadComponent handleTargetFileChange={this.handleTargetFileChange} fileList={this.state.targetFileList} cardTitle='Upload Your Own Animal Image' maxFile='1' />
                  </div>
                  <UploadComponent handleTargetFileChange={this.handleResultFileChange} fileList={this.state.sourceFileList} cardTitle='Upload Target Image (face expression you want)' maxFile='1' />
                </> :
                <>
                  <div style={{ marginRight: '48px' }} >
                    <UploadComponent handleTargetFileChange={this.handleTargetFileChange} fileList={this.state.targetFileList} cardTitle='Upload French Bulldog Image' maxFile='1' />
                  </div>
                  <UploadComponent handleTargetFileChange={this.handleResultFileChange} fileList={this.state.sourceFileList} cardTitle='Upload Japanese Spitz Image' maxFile='1' />
                </>}

            </div>
            <div style={{ margin: '30px 0', display: 'flex' }}>
              <TranslateBtn targetFileList={this.state.targetFileList} sourceFileList={this.state.sourceFileList} getResultFileList={this.getResultFileList} mode={this.state.mode} />
            </div>
            <div>
              <ShowResult resultFileList={this.state.resultFileList} mode={this.state.mode} />
            </div>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>© NUS-ISS-PRS Project</Footer>
      </Layout >
    )
  }
}


export default App;
