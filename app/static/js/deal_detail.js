document.addEventListener('DOMContentLoaded', function() {
        const statusButton = document.getElementById("status");
        const status = statusButton.textContent.trim();
        const situation = $("#situation").val();
        //商品が購入かレンタルかの判断
        let isPurchase = null;
        if(situation == "購入"){
            isPurchase = true;
        }else{
            isPurchase = false;
        }
        console.log(situation);
        console.log(isPurchase);
        updateTimeline(status,isPurchase);
        loadComments();
        loadSeller();
    });

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
const purchaseHiddenItems = [5, 6, 7,8]; // Purchase時に5,6,7,8のステップを隠す

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

const status_data = document.getElementById("status").textContent.trim().normalize();

console.log(status_data);

/////////////////////////////評価////////////////////////////////////////
console.log("evaluation function loaded");

const evaluation_block = $("#productEvaluation");

if (status_data != "取引完了"){
    evaluation_block.hide();
}else{
    evaluation_block.show();
}

let selectedRating = 4;
let isEvaluationSubmitted = false; 
const stars = document.querySelectorAll('.star');

stars.forEach(star => {
    star.addEventListener('click', function() {
        if (isEvaluationSubmitted) return;
        selectedRating = this.dataset.rating;
        updateStars(selectedRating);
    });

    star.addEventListener('mouseover', function() {
        if (isEvaluationSubmitted) return;
        updateStars(this.dataset.rating);
    });
});

document.getElementById('starsContainer').addEventListener('mouseleave', function() {
    if (isEvaluationSubmitted) return;
    updateStars(selectedRating);
});

function updateStars(rating) {
    stars.forEach(star => {
        if (star.dataset.rating <= rating) {
            star.classList.remove('empty');
        } else {
            star.classList.add('empty');
        }
    });
}

function handleSubmit() {
    const evaluation = selectedRating;
    axios.post('/deal/evaluation',{
        evaluation:evaluation,
        transaction_id: document.getElementById('transaction_id').value 
        }
     )
     .then(response=>{
        isEvaluationSubmitted = true;
        const submitButton = document.querySelector('button[onclick="handleSubmit()"]');
        if (submitButton) {
            submitButton.style.display = 'none';  // 隠す
            //submitButton.remove() 
        }
        const evaluationCheck = document.getElementById('evaluation_check');
        if (evaluationCheck) {
            evaluationCheck.textContent = '✓ 評価が完了しました';
            evaluationCheck.style.color = '#252525ff';
        }
        
        // star禁止
        stars.forEach(star => {
            star.style.cursor = 'default';  // 
        }); 
        alert(`${selectedRating}つ星で評価しました`);
        //window
     })
    .catch(error => {
        console.error('Error:', error);
        alert('評価の送信に失敗しました');
    });
}

// 初期表示
updateStars(selectedRating);

/////////////////////////seller DATA  ////////////////////////////////


/////////////////////////// render seller DATA  ///////////////////////
function renderSellerProfile(response){
  const sellerData = response.data;
  const container = document.getElementById('profileContainer');
  const sellerInfo = sellerData.firstName;
  const sellerImg = sellerData.profileImage;
  const sellerStatus = sellerData.status;
  const sellerSmoker = sellerData.smoker;
  const sellerCount = sellerData.evaluation_count;
  const sellerScore = parseFloat(sellerData.average_score);

  //STAR//
  const stars = generateStars(sellerScore || 0);
  const statusBadge = sellerStatus === '本人確認済み' ? '本人確認済み' : '未承認';
  const smokerBadge = sellerSmoker == 0 ? '非喫煙者':'喫煙者';

  const profileHTML = `
   <div class="img-name w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center overflow-hidden">
      <img src="/static/img/${sellerImg}" 
                 alt="プロフィール画像"
                 class="profile-image w-full h-full object-cover">
    </div>

    <div class="profile-name">
        <p class="font-semibold text-lg">${sellerInfo}</p>
        <div class="profile-rating flex items-center gap-2 mt-1">
          <div>
            <span class="stars">${stars}</span>
          </div>
          <span class="rating-count text-sm text-gray-600">${sellerCount || 0}</span>
        </div>
        
        <div class="badge-group flex items-center gap-2 mt-1">
          <i id="checkMark" class="fas fa-check-circle text-green-500 text-sm"></i>  
          <p class="text-xs text-gray-600">${statusBadge}</p>
          <span class="badge text-xs text-gray-600">${smokerBadge}</span>
        </div> 
    </div>
        
        
        
    `;  
    container.innerHTML = profileHTML;
}

/////////////////////////  Score Star //////////////////////////////////////////
function generateStars(count) {
    let stars = '';
    for (let i = 0; i < count; i++) {
        stars += '★';
    }
    for (let i = 0; i < 5 - count; i++) {
        stars += '☆';
    }
    return stars;
}

////////////////////////// SHOW ERROR /////////////////////////////////////////
function showError(message) {
    const container = document.getElementById('profileContainer');
    container.innerHTML = `
        <div class="error-message">
            <p>${message}</p>
        </div>
    `;
}
 // /////////////////////// load comments //////////////////////////////


function loadComments() {
    // const transactionID = document.getElementById('transactionID').value;
    const productID = document.getElementById('productID').value;
    fetch(`/deal/get-comments?product_id=${productID}`)
        .then(response => response.json())
        .then(data => {
            console.log('Comments loaded:', data);
            renderComments(data);
        })
        .catch(error => console.error('Error loading comments:', error));
}

// render comments to page
function renderComments(comments) {
    const container = document.getElementById('commentsContainer');
    const account = 
    container.innerHTML = comments.map(comment => `
        <div class="border rounded-xs p-6 mb-6">
            <p class="font-semibold">${comment.firstName}</p>
            <p class="text-gray-700 mt-2">${comment.content}</p>
            <p class="text-gray-400 text-sm mt-2">${new Date(comment.createdDate).toLocaleString('ja-JP')}</p>
        </div>
    `).join('');
}

// 新しい comment　提出
function submitComment() {
    const productID = document.getElementById('productID').value;
    const content = document.getElementById('commentInput').value.trim();

    if (!content) {
        return;
    }

    // バックエンドに送る
    fetch('/deal/add-comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productID,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Comment added:', data);
            
            // clear 
            document.getElementById('commentInput').value = '';
            
            //  comments reload
            loadComments();
            
            alert('メッセージを送信しました');
        } else {
            alert('エラー: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('送信に失敗しました');
    });
}