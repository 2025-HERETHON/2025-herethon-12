const KAKAO_REST_API_KEY = "";
// 여기에 카카오 REST API 키 담아서 테스트

const region = document.getElementById("region");
const submitBtn = document.querySelector(".submit-btn");
const searchBtn = document.querySelector(".search-btn");
const resultBtn = document.querySelector(".result-btn");
const cityInput = document.getElementById("region_city");
const districtInput = document.getElementById("region_district");
const dongInput = document.getElementById("region_dong");
const form = document.querySelector("form");

let regionCity = "";
let regionDistrict = "";
let regionDong = "";
resultBtn.disabled = true;

// input에 값 들어오면 동네 인증 완료 버튼 색 변함
region.addEventListener("input", () => {
  if (region.value) {
    submitBtn.style.backgroundColor = "var(--color-main)";
  } else {
    submitBtn.style.backgroundColor = "#8A8A8A";
  }
});

// 버튼 색 관련
submitBtn.addEventListener("click", () => {
  submitBtn.style.backgroundColor = "var(--color-deep-main)";
});

// 현재 위치로 검색 버튼 누르면 gps로 인증
searchBtn.addEventListener("click", getLocation);

// 위도, 경도 구하기
function getLocation() {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      getRegionFromCoords(lat, lon);
    },
    (error) => {
      resultBtn.textContent = "브라우저가 위치 정보를 지원하지 않음";
    }
  );
}

// 위도, 경도 -> 카카오 API
async function getRegionFromCoords(lat, lon) {
  try {
    const response = await fetch(
      `https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=${lon}&y=${lat}`,
      {
        headers: {
            Authorization: `KakaoAK ${KAKAO_REST_API_KEY}`,
        },
      }
    );

    const data = await response.json();
    if (data.documents.length > 0) {
      const region = data.documents[0];
      regionCity = region.region_1depth_name;
      regionDistrict = region.region_2depth_name;
      regionDong = region.region_3depth_name;
      resultBtn.textContent = `${regionCity} ${regionDistrict} ${regionDong}`;
      // 지역명 적힌 버튼 누를 수 있음
      resultBtn.disabled = false;
    } else {
      // 지역명 버튼 막아둠
      resultBtn.textContent = "지역 정보를 찾을 수 없음";
      resultBtn.disabled = true;
    }
  } catch (err) {
    console.error("카카오 API 호출 오류:", err);
  }
}

// 지역명 버튼 누르면 자동으로 input으로 들어감
resultBtn.addEventListener("click", () => {
  region.value = `${regionCity} ${regionDistrict} ${regionDong}`;
  cityInput.value = regionCity;
  districtInput.value = regionDistrict;
  dongInput.value = regionDong;
  region.dispatchEvent(new Event("input")); // input 이벤트 강제 발생 -> 버튼 색 변경
});

// input 값 없으면 submit 안 됨
form.addEventListener("submit", (e) => {
  if (!region.value) {
    e.preventDefault();
    alert("지역 인증을 완료해주세요.");
  }
});
