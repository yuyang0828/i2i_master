import React from 'react';
import { Image, Card } from 'antd';

class ShowResult extends React.Component {

    render() {
        // console.log(this.props.resultFileList.lengh)
        // undefined?
        return (
            this.props.resultFileList[0] ? (
                this.props.mode == 'cnn' ?
                    <Card title='Result Image'>
                        <Image
                            // width={200}
                            src={this.props.resultFileList[0]}
                        />
                    </Card> :
                    <div style={{ display: 'flex' }}>
                        <Card title='Japanese Spitz Image' style={{ marginRight: '48px' }}>
                            <Image
                                // width={200}
                                src={this.props.resultFileList[0]}
                            />
                        </Card>
                        <Card title='French Bulldog Image'>
                            <Image
                                // width={200}
                                src={this.props.resultFileList[1]}
                            />
                        </Card>
                    </div>
            ) : null
        )
    }
}

export default ShowResult

