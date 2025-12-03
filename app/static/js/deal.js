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

//コンタンツswitch toggle
 function switchTab(tabIndex) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');
    tabs.forEach((tab, index) => {
        tab.classList.toggle('active', index === tabIndex);
    });
    
    contents.forEach((content, index) => {
        content.classList.toggle('active', index === tabIndex);
    });
    buttons.forEach((button,index) =>{
        button.classList.toggle('active',index === tabIndex);
    });
}

//right area
let currentProductId = null;

document.querySelectorAll('.product-item').forEach(item => {
  item.addEventListener('click', function() {
    // Remove highlight from all items
    document.querySelectorAll('.product-item').forEach(el => {
      el.classList.remove('bg-blue-50', 'border-blue-400');
    });
    
    // Add highlight to clicked item
    this.classList.add('bg-blue-50', 'border-blue-400');
    
    // Get product data
    const productData = JSON.parse(this.dataset.product);

    //今のIDを保存
    currentProductId = productData.id;
    
    // Update right area with product details
    // document.getElementById('detailProductName').textContent = productData.name || '商品名なし';
    document.getElementById('detailProductExplanation').textContent = productData.explanation || '説明文なし';
    
    // document.getElementById('detailProductSituation').textContent = productData.situation || '-';
    // document.getElementById('detailProductStatus').textContent = productData.status || '-';
    
    // Update image if available
    if (productData.img) {
      const basePath = "/static/img/productImg/";
      document.getElementById('detailProductImg').src = basePath + productData.img;
    }
    //商品が購入かレンタルかの判断
    let isPurchase = null;
    if(productData.situation == "購入"){
      isPurchase = true;
      $('#rentalBuy').hide();
    }else{
      isPurchase = false;
      $('#rentalBuy').show();
    }
    console.log(productData.situation);
    console.log(isPurchase);
    
    updateTimeline(productData.status,isPurchase);

    const transactionId = productData.transaction_id || productData.id;
    document.getElementById('detailTransactionId').textContent = transactionId;

    const activeCheck = $("button.active").text();
    console.log(activeCheck);
    
    const dealDetailUrl = `/deal/deal/${transactionId}`;
    document.getElementById('dealDetailLink').href = dealDetailUrl;

    const dealDetailSellerUrl = `/deal/deal_seller/${transactionId}`;
    document.getElementById('dealDetailSellerLink').href = dealDetailSellerUrl;

    console.log("start_date:",productData.date);
    const date = new Date(productData.date);
    console.log("date",date); 
    const dateOnly = date.toISOString().split('T')[0];
    console.log("dateOnly",dateOnly);
    const timeOnly = date.toTimeString().split(' ')[0];
    console.log("timeOnly",timeOnly);
    const formattedTime = `${dateOnly} ${timeOnly}`;
    console.log("formattedTime",formattedTime);   
    $("#start_date").empty().append(
      `<span class="text-gray-600 text-xs" id="startDate">${formattedTime}</span>`
    );
  });
});

// Auto-select first product on load
window.addEventListener('DOMContentLoaded', function() {
  const firstProduct = document.querySelector('.product-item');
  if (firstProduct) {
    firstProduct.click();
  }
});

//purchaseFlgの判断
// document.addEventListener('DOMContentLoaded',function(){
//     // 購入レンタル判断
//   let isPurchase = null;
//   if (productData.status === "購入"){
//     isPurchase = true;
//   }
//   else{
//     isPurchase = false;
//   }
// })

//medium area
const rentalStatusMap = {
  '支払い待ち': 1,
  '発送待ち': 2,
  '配達中': 3,
  '到着': 4,
  'レンタル中': 5,
  'クリーニング期間': 6,
  '返送待ち': 7,
  '返送中':8,
  '取引完了': 9
};

const purchaseStatusMap = {
  '支払い待ち': 1,
  '発送待ち': 2,
  '配達中': 3,
  '到着': 4,
  '取引完了': 9
};
const statusMap = {
  '支払い待ち': 1,
  '発送待ち': 2,
  '配達中': 3,
  '到着': 4,
  'レンタル中': 5,
  'クリーニング期間': 6,
  '返送待ち': 7,
  '返送中':8,
  '取引完了': 9
};

const rentalHiddenItems = []; // Rental時にすべてのステップを表示
const purchaseHiddenItems = [5, 6, 7,8]; // Purchase時に5,6,7のステップを隠す

function updateTimeline(status,isPurchase=false) {
  //商品のレンタル購入を判断し、ステータスの項目を変える
  const statusMap = isPurchase ? purchaseStatusMap : rentalStatusMap;
  const hiddenItems = isPurchase ? purchaseHiddenItems : rentalHiddenItems;

  const step = statusMap[status] || 0;
  
  // 進捗状況
  for (let i = 1; i <= 9; i++) {
    const timelineItem = document.querySelector(`.timeline-item-${i}`);
    // const circles = document.querySelectorAll(`.timeline-item-${i} .timeline-circle`);
    if (!timelineItem) continue;

     if (hiddenItems.includes(i)) {
      timelineItem.style.display = 'none';
    } else {
      timelineItem.style.display = 'flex';
    }
    
    const circles = timelineItem.querySelectorAll('.timeline-circle'); 

    if (i < step) {
      // Completed steps - show checkmark
      circles.forEach(circle => {
        circle.classList.remove('bg-white', 'border-2', 'border-gray-400', 'text-gray-600');
        circle.classList.add('bg-gray-800', 'text-white');
        circle.innerHTML = '✓';
      });
    } else if (i === step) {
      // Current step - show number with highlight
      circles.forEach(circle => {
        circle.classList.remove('bg-white', 'border-2', 'border-gray-400', 'text-gray-600');
        circle.classList.add('bg-gray-800', 'text-white');
        circle.innerHTML = i;
      });
    } else {
      // Future steps - show number
      circles.forEach(circle => {
        circle.classList.remove('bg-gray-800', 'text-white');
        circle.classList.add('bg-white', 'border-2', 'border-gray-400', 'text-gray-600');
        circle.innerHTML = i;
      });
    }
  }
}

function rentalBuy(product_id){
  window.location.href=`/products/purchase/${product_id}`;
}
