function updateCurrentTime() {
    var currentTime1Element = document.getElementById("current-time1");
    var currentTime2Element = document.getElementById("current-time2");
    var currentDate = new Date();

    var year = currentDate.getFullYear();
    var month = currentDate.getMonth() + 1;
    var day = currentDate.getDate();
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();

    if (month < 10) {
        month = "0" + month.toString();
    }

    if (hours < 10) {
        hours = "0" + hours.toString();
    }

    if (minutes < 10) {
        minutes = "0" + minutes.toString();
    }

    if (seconds < 10) {
        seconds = "0" + seconds.toString();
    }

    var formattedTime1 = year + "-" + month + "-" + day;
    var formattedTime2 = hours + ":" + minutes + ":" + seconds;
    currentTime1Element.textContent = formattedTime1;
    currentTime2Element.textContent = formattedTime2;
}

window.onload = () => {
    // 获取后台数据
    let url = "./rf/"

    let collection_data = undefined;

    // 请求头
    const server_key = "CollectionServer";

    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    headers.append("X-Server-Key", server_key);
    headers.append('X-CSRFToken', csrfToken);

    // 请求体
    const requestBody = {
        type: "CollectionDataRequest",
    };


    // 构建 fetch 请求
    const fetchOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestBody)
    };


    // 发起请求
    fetch(url, fetchOptions)
        .then(response => response.json())
        .then(data => {
            collection_data = data.data;
            // 创建表格元素
            const table = document.createElement('table');
            table.className = 'fade-in';

            // collection_data 数据格式
            // const data = [
            //     { imgSrc: 'image1.jpg', name: 'Item 1', rating: '4.5', link: 'https://example.com/item1' },
            //     { imgSrc: 'image2.jpg', name: 'Item 2', rating: '3.8', link: 'https://example.com/item2' },
            //     { imgSrc: 'image3.jpg', name: 'Item 3', rating: '4.2', link: 'https://example.com/item3' },
            //     // ... 添加更多数据项
            // ];

            var column_count = 5
            var row_count = Math.ceil(collection_data.length / column_count)
            var item_count = 0

            // 创建表格行和单元格
            for (let i = 0; i < row_count && item_count < collection_data.length; i++) {
                const row = table.insertRow();
                for (let j = 0; j < 5 && item_count < collection_data.length; j++) {
                    const cell = row.insertCell();
                    // 创建内容块
                    const item = document.createElement('div');
                    item.style.textAlign = 'center';

                    // 创建图片块
                    const imgLink = document.createElement('a');
                    imgLink.href = collection_data[i * 5 + j].link;
                    const imgDiv = document.createElement('div');
                    const img = document.createElement('img');
                    img.src = collection_data[i * 5 + j].imgSrc;
                    imgLink.appendChild(img);
                    imgDiv.appendChild(imgLink);

                    // 创建文字链接块
                    const textDiv = document.createElement('div');
                    const name = document.createElement('a');
                    name.href = collection_data[i * 5 + j].link;
                    name.textContent = collection_data[i * 5 + j].name;

                    const rating = document.createElement('div');
                    if (collection_data[i * 5 + j].rating === null) {
                        rating.textContent = `评分: -`;
                    } else {
                        rating.textContent = `评分: ${collection_data[i * 5 + j].rating.score}`;
                    }
                    rating.id = 'rating';
                    textDiv.appendChild(name);
                    textDiv.appendChild(rating);

                    // 将图片块和文字链接块添加到内容块
                    item.appendChild(imgDiv);
                    item.appendChild(textDiv);

                    // 将内容块添加到单元格
                    cell.appendChild(item);
                    item_count++;
                }
            }

            // 将表格添加到页面中
            document.getElementById('main').appendChild(table);

            setTimeout(() => {
                table.style.opacity = 1;
            }, 10);
        })
        .catch(error => {
            console.error("Error", error);
        });


    // 监听标头
    const stickyHeadDiv = document.getElementById('head-div');

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const opacity = calculateOpacity(scrollTop);
        stickyHeadDiv.style.opacity = opacity;
    });

    function calculateOpacity(scrollTop) {
        if (scrollTop > 100) {
            // 向下滚动，透明度降低
            return 1;
        } else {
            // 向上滚动，透明度增大
            return 0;
        }
    }

    // 每隔一秒更新一次时间
    setInterval(updateCurrentTime, 1000);

    // 初始加载时先更新一次时间
    updateCurrentTime();
}