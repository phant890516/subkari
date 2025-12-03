document.addEventListener('DOMContentLoaded', function() {
        const statusButton = document.getElementById("status");
        const status = statusButton.textContent.trim();

        $("#cleaningTimer").toggle(status == "クリーニング期間");
        $("#shippingPhotoContainer").toggle(status == "発送待ち");
        $("#receivedPhotoContainer").toggle(status == "レンタル中");
        $("#returnReceivedPhotoContainer").toggle(status == "返送中");

    });

//Timer
function startTimer() {
    let hours = 12, minutes = 59, seconds = 59;
    const timerEl = document.getElementById('timer');

    setInterval(() => {
        if (seconds > 0) {
            seconds--;
        } else if (minutes > 0) {
            minutes--;
            seconds = 59;
        } else if (hours > 0) {
            hours--;
            minutes = 59;
            seconds = 59;
        }

        const h = String(hours).padStart(2, '0');
        const m = String(minutes).padStart(2, '0');
        const s = String(seconds).padStart(2, '0');
        timerEl.textContent = `${h}:${m}:${s}`;
    }, 1000);
}

startTimer();

//shipping Image Upload
document.getElementById('uploadBtn').addEventListener('click', async function() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('ファイルを選択してください');
        return;
    }
    
    // 取得 transaction_id
    const transactionId = document.querySelector('[data-transaction-id]').dataset.transactionId; //  transaction id
    console.log("transactionID get",transactionId);
    
    const formData = new FormData();
    formData.append('img', file);
    
    try {
        const response = await axios.post(
            `/deal/list/shipping/imageUpload/${transactionId}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        );
        
        if (response.data.success) {
            
            document.getElementById('uploadMessage').innerHTML = 
                `<p style="color: green;">${response.data.message}</p>`;
            
            // 画像表示
            const img = document.getElementById('uploadedImage');
            img.src = response.data.image_url;
            img.style.display = 'block';
            
            // クリア
            fileInput.value = '';
            window.location.href = `/deal/deal/${transactionId}`
        }
    } catch (error) {
        const errorMsg = error.response?.data?.error || '未知のエラーが発生しました';
        document.getElementById('uploadMessage').innerHTML = 
            `<p style="color: red;">${errorMsg}</p>`;
    }
});

//return received Image Upload
document.getElementById('uploadReturnReceivedBtn').addEventListener('click', async function() {
    const fileInput = document.getElementById('imageReturnReceivedInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('ファイルを選択してください');
        return;
    }
    
    // 取得 transaction_id
    const transactionId = document.querySelector('[data-transaction-id]').dataset.transactionId; // transaction id
    
    const formData = new FormData();
    formData.append('img', file);
    
    try {
        const response = await axios.post(
            `/deal/list/returnReceived/imageUpload/${transactionId}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        );
        
        if (response.data.success) {
            document.getElementById('uploadReturnReceivedMessage').innerHTML = 
                `<p style="color: green;">${response.data.message}</p>`;
            
            // 画像表示
            const img = document.getElementById('uploadedReturnReceivedImage');
            img.src = response.data.image_url;
            img.style.display = 'block';
            
            // クリア
            fileInput.value = '';
            window.location.href = `/deal/deal/${transactionId}`
        }
    } catch (error) {
        const errorMsg = error.response?.data?.error || '未知のエラーが発生しました';
        document.getElementById('uploadReturnReceivedMessage').innerHTML = 
            `<p style="color: red;">${errorMsg}</p>`;
    }
});

// 取得 customer_id
const customerId = document.querySelector('[data-customer-id]').dataset.customerId; // customer id
console.log("customerID",customerId);

function loadSeller(){
  axios.get(`/deal/seller_data/get/${customerId}`)
    .then(response=>{
      console.log('seller_data:',response.data);
      if (response.data.success){

        renderSellerProfile(response.data);
      }else{
        showError('no data found.');
      }
    })
    .catch(error=>{
      console.log('CATCH ERROR',error);
      showError('出品者データエラー');
    });
}