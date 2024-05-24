function compressImp(file, resolve, reject)
{
    if (file.type.indexOf("image") === 0) {
        let reader = new FileReader(),
            img = new Image();

        // 将 file 读取成 Data url
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            // 用 Data url 构造 image
            img.src = e.target.result;
        };

        img.onload = function () {
            let canvas = document.createElement('canvas');
            let context = canvas.getContext('2d');

            // 图片原始尺寸
            let originWidth = this.width;
            let originHeight = this.height;

            // 最大尺寸限制，可通过设置宽高来实现图片压缩程度
            let maxWidth = 2500,
                maxHeight = 2500;
            // 目标尺寸
            let targetWidth = originWidth,
                targetHeight = originHeight;
            // 图片尺寸超过限制
            if (originWidth > maxWidth || originHeight > maxHeight) {
                if (originWidth / originHeight > maxWidth / maxHeight) {
                    // 更宽，按照宽度限定尺寸
                    targetWidth = maxWidth;
                    targetHeight = Math.round(maxWidth * (originHeight / originWidth));
                } else {
                    targetHeight = maxHeight;
                    targetWidth = Math.round(maxHeight * (originWidth / originHeight));
                }
                // canvas对图片进行缩放
                canvas.width = targetWidth;
                canvas.height = targetHeight;
                // 清除画布
                context.clearRect(0, 0, targetWidth, targetHeight);
                // 用image 绘制 canvas
                context.drawImage(img, 0, 0, targetWidth, targetHeight);

                // 非 IE，返回 File对象
                if(canvas.toBlob){
                    canvas.toBlob((blob)=>{
                        let newFile = new File([blob], file.name); // IE 下无法构造 File 对象
                        resolve(newFile);
                    }, 'image/jpeg', 0.92);
                }
                else{  // 兼容IE，返回Base64
                    let dataUrl = canvas.toDataURL('image/jpeg', 0.92);
                    resolve(dataUrl);
                }
            }
            else{
                resolve(file);
            }
        };
    }
    else{
        reject();
    }
}
export default function compress(file){
    return new Promise(function(resolve, reject) {
        compressImp(file, resolve, reject)
    });
}
