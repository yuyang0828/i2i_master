import React from 'react';
import { Button } from 'antd';
import axios from 'axios';


class TranslateBtn extends React.Component {
    onBtnClick = () => {


        const formData = new FormData()
        let fileObjList1 = this.props.targetFileList.map((f) => f.originFileObj);
        let fileObjList2 = this.props.sourceFileList.map((f) => f.originFileObj);
        formData.append('my_animal', fileObjList1[0])
        formData.append('target', fileObjList2[0])

        if (this.props.mode == 'cnn') {
            axios({
                url: '/faceai',
                method: 'post',
                data: formData,
                responseType: 'blob',
                headers: { 'Content-Type': 'multipart/form-data' }
            }).then(res => {
                // two kinds response
                // ====== byte stream
                // let myBlob = new Blob([res.data], { type: "image/jpeg" })
                console.log(res)
                let imgUrl = URL.createObjectURL(res.data)
                this.props.getResultFileList([imgUrl])

                //======= base64
                // let base64url = 'data:image/jpeg;base64,' + res.data
                // this.props.getResultFileList([base64url]])
            })
        } else {
            axios({
                url: '/faceaigan1',
                method: 'post',
                data: formData,
                responseType: 'blob',
                headers: { 'Content-Type': 'multipart/form-data' }
            }).then(res => {

                let imgUrl1 = URL.createObjectURL(res.data)
                return imgUrl1

            }).then(url1 => {
                axios({
                    url: '/faceaigan2',
                    method: 'post',
                    data: formData,
                    responseType: 'blob',
                    headers: { 'Content-Type': 'multipart/form-data' }
                }).then(res => {
                    let imgUrl2 = URL.createObjectURL(res.data)
                    this.props.getResultFileList([url1, imgUrl2])
                })
            })
        }


    }

    render() {
        return (
            <>
                <Button type="primary" onClick={this.onBtnClick}>Translate</Button>
            </>
        )
    }


}

export default TranslateBtn