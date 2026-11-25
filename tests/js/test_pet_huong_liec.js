/* Linh vật lúc KHÔNG theo con trỏ phải liếc VÀO TRONG màn hình, theo mép nó đang nép.

       node tests/js/test_pet_huong_liec.js

   Nép mép PHẢI thì liếc sang TRÁI, nép mép TRÁI thì liếc sang PHẢI. Trước 0.59.11 hướng liếc
   là một hằng số luôn dương (NGHI_X), nên con pet đứng ở mép phải lại nhìn trổ ra ngoài viền
   màn hình, trông như đang quay lưng lại với trang đang đọc.

   Vì sao phải CHẠY THẬT chứ không dò mã nguồn: hướng liếc chỉ hiện ra sau khi vòng vẽ
   requestAnimationFrame nội suy dần về đích, và vòng đó có ba cái chốt giết nó trong im lặng
   (prefers-reduced-motion, tab bị ẩn, con trỏ vừa động trong 1,6 giây). Dò chữ trong mã thì cả
   ba ca hỏng đó vẫn xanh. Bộ DOM giả ở đây lấy nguyên cách làm của test_pet_mat_dang_nghi.js.

   KHÔNG dùng ký tự em dash. */
const path = require("path");
const root = path.join(__dirname, "..", "..");

let fails = [];
function check(name, cond) { console.log((cond ? "ok   " : "FAIL ") + name); if (!cond) fails.push(name); }

function nutGia() {
  const n = {
    innerHTML: "", hidden: false, dataset: {}, childElementCount: 1,
    style: { setProperty() {}, removeProperty() {} },
    classList: { add() {}, remove() {}, contains: () => false, toggle() {} },
    setAttribute() {}, getAttribute: () => null, addEventListener() {}, appendChild() {},
    getBoundingClientRect: () => ({ top: 0, left: 0, right: 0, bottom: 0, width: 56, height: 56 }),
    querySelectorAll: () => [], focus() {},
  };
  n.querySelector = () => n;
  return n;
}

const nut = {
  ".pet-body": nutGia(), ".pet-menu": nutGia(), ".pet-rig": nutGia(),
  ".pet-ring": nutGia(), ".pet-face": nutGia(), ".pet-eyes": nutGia(), svg: nutGia(),
};
const goc = nutGia();
goc.querySelector = (sel) => nut[sel] || null;

let dongHo = 1000;
let khungCho = null;
const mqGiam = { matches: false, addEventListener() {}, addListener() {} };

global.window = {
  t: (k, d) => d || k,
  ic: () => "",
  innerWidth: 1280, innerHeight: 900,
  matchMedia: () => mqGiam,
  addEventListener() {}, dispatchEvent() {},
  requestAnimationFrame: (fn) => { khungCho = fn; return 1; },
  cancelAnimationFrame: () => { khungCho = null; },
};
global.document = {
  readyState: "complete", hidden: false,
  createElement: () => goc,
  getElementById: () => null,
  addEventListener() {},
  body: { appendChild() {} },
  querySelectorAll: () => [],
};
global.localStorage = { getItem: () => null, setItem() {}, removeItem() {} };
global.performance = { now: () => dongHo };
global.requestAnimationFrame = window.requestAnimationFrame;
global.cancelAnimationFrame = window.cancelAnimationFrame;
global.fetch = () => new Promise(() => {});      // không bao giờ trả lời: giữ nguyên cfg đang có
global.CustomEvent = function () {};
global.FormData = function () { this.append = function () {}; };

// Gieo Math.random CỐ ĐỊNH trước khi nạp pet.js. pet.js chọn đích liếc bằng
// nghiX() + (Math.random() * 2 - 1) * 0,17, nên để ngẫu nhiên thì mỗi bước dưới đây kết thúc ở
// một chỗ khác nhau, và phép đo "đổi mép thì lật ngay" ở bước 3 lúc thì kịp qua mốc, lúc thì
// dừng cách mốc một hai phần mười: đo thật thì chập chờn 3 lượt đỏ trên 150 lượt chạy.
// Chọn đúng 0,5 vì nó làm số hạng nhiễu bằng 0 tuyệt đối: đích liếc trùng khít dáng nghỉ, hai
// mép thành ẢNH GƯƠNG của nhau, nhờ vậy quãng đường lật mép mới đo được chính xác. Biên nhiễu
// đảo mắt không phải thứ phép kiểm này canh, bỏ nó đi không mất gì.
Math.random = () => 0.5;

require(path.join(root, "dashboard", "pet.js"));
const P = window.JavisPet;
check("pet.js nạp được với DOM giả", !!P && typeof P.setCfg === "function");

// Tầm đưa mắt theo TRỤC NGANG đang được vẽ ra, đơn vị px trong viewBox. Âm = nhìn sang trái.
function nhinNgang() {
  const tf = nut[".pet-eyes"].style.transform || "";
  const m = /translate\(([-\d.]+)px/.exec(tf);
  return m ? Number(m[1]) : null;
}

// Quay đồng hồ và gọi từng khung hình. Mỗi khung nhảy 200ms nhưng pet.js chặn dt ở 0,05s, nên
// phải đủ nhiều khung cho phép nội suy về đích (hằng thời gian của nhịp nghỉ là 1/1,2 giây).
async function quay(soBuoc) {
  for (let i = 0; i < soBuoc; i++) {
    dongHo += 200;
    const fn = khungCho; khungCho = null;
    if (fn) fn(dongHo);
    await new Promise((r) => setTimeout(r, 0));
  }
  return nhinNgang();
}

(async () => {

// ---- 1. Mép PHẢI (mặc định): liếc sang TRÁI ----
check("mặc định pet nép mép phải", P.get().side === "right");
const phai = await quay(140);
check("nép mép phải thì nhìn sang TRÁI, vào trong màn hình (x=" + phai + ")", phai !== null && phai < -1);

// ---- 2. Mép TRÁI: liếc sang PHẢI ----
P.setCfg({ side: "left" });
const trai = await quay(140);
check("nép mép trái thì nhìn sang PHẢI, vào trong màn hình (x=" + trai + ")", trai !== null && trai > 1);

// ---- 3. Đổi mép được gom và áp dụng ở khung hình kế tiếp ----
// setCfg chỉ đánh dấu hướng mới; mắt được cập nhật trong vòng requestAnimationFrame kế tiếp.
// Đừng yêu cầu nội suy hoàn tất trong khung đầu: chuyển động mượt sẽ đi qua nhiều khung.
const dichLat = -trai;            // dáng liếc hai mép là ảnh gương của nhau, xem nghiX()
P.setCfg({ side: "right" });
const khungDau = await quay(1);
check("khung kế tiếp sau đổi mép vẫn giữ được giá trị mắt hợp lệ", khungDau !== null && Number.isFinite(khungDau));
const ngay = await quay(14);      // tổng 3 giây, ngắn hơn một nhịp đảo mắt
const diDuoc = ngay === null ? 0 : (trai - ngay) / (trai - dichLat);
check("trong 3 giây mắt đi được quá nửa quãng sang mép kia (x=" + ngay + ", " +
  (diDuoc * 100).toFixed(1) + "% quãng)", diDuoc > 0.5);

// ---- 4. Tắt hiệu ứng thì mắt đứng nguyên ----
// prefers-reduced-motion là một trong ba cái chốt làm vòng vẽ thoát sớm, và cũng là ca mà dò
// mã nguồn không bao giờ bắt được, nên canh luôn ở đây.
mqGiam.matches = true;
const tatHieuUng = nhinNgang();
await quay(10);
check("tắt hiệu ứng (prefers-reduced-motion) thì mắt đứng yên", nhinNgang() === tatHieuUng);

if (fails.length) { console.log("\nFAIL:", fails.length, fails); process.exit(1); }
console.log("\nOK - hướng liếc của linh vật");
})();
