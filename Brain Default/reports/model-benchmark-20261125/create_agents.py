"""Create isolated benchmark-qualified agents, never overwrite existing agents."""
import json
import pathlib
import statistics
import yaml

ROOT=pathlib.Path(__file__).resolve().parent
VAULT=ROOT.parent.parent
summary=json.loads((ROOT/'summary.json').read_text(encoding='utf-8'))
configs=[
 ('shopdonk-sonnet-review','ShopDonk Sonnet - Rà soát logic','claude-sonnet-4-6','Rà soát logic và đặc tả của đoạn mã ngắn do người dùng cung cấp.','Chỉ kết luận lỗi khi chỉ ra đầu vào, nhánh mã và đầu ra sai; phân biệt lỗi với thiếu đặc tả.'),
 ('shopdonk-luna-analysis','ShopDonk Luna - Phân tích có cấu trúc','gpt-6-luna','Phân tích yêu cầu nhỏ và tạo kết quả có cấu trúc, có căn cứ.','Tách dữ kiện, giả định và phần thiếu; không suy rộng từ ví dụ nhỏ thành kết luận tổng quát.'),
 ('shopdonk-sol-test','ShopDonk Sol - Kiểm thử tác vụ ngắn','gpt-5.6-sol','Thiết kế ca kiểm thử và kiểm tra đoạn mã, dữ liệu nhỏ.','Nêu Sample Input, Expected Output và ca biên; chỉ báo đã chạy khi có bằng chứng từ công cụ.'),
 ('shopdonk-deepseek-data','ShopDonk DeepSeek - Kiểm tra số liệu nhỏ','deepseek-v4.1-flash','Kiểm tra phép tính và tổng hợp dữ liệu có phạm vi rõ.','Nêu công thức, đơn vị, phạm vi; dữ liệu lớn phải dùng công cụ tính thay vì nhẩm.'),
 ('shopdonk-gemini-draft','ShopDonk Gemini - Bản nháp cần kiểm tra','gemini-flash-3.8-high','Soạn bản nháp văn bản đơn giản để người dùng hoặc model khác kiểm tra.','Chưa đủ điều kiện dùng độc lập cho số liệu hoặc kiểm tra code: benchmark có một kết quả rỗng và một phép tính sai.'),
 ('shopdonk-grok-check','ShopDonk Grok - Kiểm tra tính nhất quán','grok-4.7','Kiểm tra mâu thuẫn và dữ kiện thiếu trong văn bản ngắn.','Không nhận có dữ liệu thời gian thực nếu chưa có công cụ hoặc nguồn; không dùng cho phản hồi cần độ trễ thấp.'),
]
created=[]
for slug,name,model,role,specific in configs:
    evidence=next(x for x in summary if x['model']==model)
    meta={'type':'agent','name':name,'slug':slug,'role':role,'tags':['AI','ShopDonk','Thử nghiệm'],'skills':[],'model':model,'model_provider':'openai-compat','updated':'2026-11-25'}
    body=f'''Bạn là {name}. Mục tiêu: {role}
Bối cảnh: trợ lý thử nghiệm qua endpoint ShopDonk đang cấu hình; không thay thế Hội đồng hay Javis Core.
Bằng chứng: benchmark 2026-11-25 đạt {evidence['passed']}/5, trung vị {evidence['median_seconds']} giây; chỉ là 5 bài nhỏ, không chứng nhận năng lực chuyên sâu.
Phạm vi tốt: đầu ra ngắn, dữ liệu người dùng cung cấp, nhiệm vụ có thể kiểm chứng.
1. Xác định đầu vào, đầu ra và tiêu chí hoàn tất; nếu thiếu dữ kiện quan trọng thì hỏi một câu.
2. Đọc đúng dữ liệu cần thiết, không quét bộ não hay gửi bí mật ra dịch vụ ngoài.
3. {specific}
4. Kiểm tra lại đáp án theo dữ kiện; không lấy tên model làm bằng chứng năng lực.
5. Trả kết luận trước, sau đó bằng chứng và tối đa ba bước tiếp theo; tiếng Việt, gọn, không em dash.
Nếu cần JSON, trả đúng schema, không kèm giải thích bên ngoài JSON.
Nếu công cụ lỗi hoặc nội dung rỗng, báo nguyên nhân quan sát được và phần việc chưa làm; không giả vờ thành công.
Không tự chuyển provider, tăng quyền, tạo lịch, giao việc nền hay chi tiêu ngoài nhiệm vụ đã được chủ giao.
Không đặt lệnh giao dịch, sửa tài khoản, gửi tin hoặc đăng nội dung khi chưa được chủ cho phép rõ ràng.
Không công bố dữ liệu thời gian thực, kết quả test hoặc giá API khi chưa có bằng chứng.
Giới hạn trong prompt không thay thế timeout và ngân sách được gateway cưỡng chế.
'''
    text='---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False)+'---\n'+body
    assert '\u2014' not in text and yaml.safe_load(text.split('---')[1])['model_provider']=='openai-compat'
    dest=VAULT/'agents'/(slug+'.md')
    if dest.exists(): raise RuntimeError('Existing agent requires review: '+slug)
    created.append((dest,text,meta))
for dest,text,meta in created:
    with dest.open('x',encoding='utf-8') as f: f.write(text)
    parsed=yaml.safe_load(dest.read_text(encoding='utf-8').split('---')[1])
    assert parsed['model']==meta['model'] and parsed['tags']
manifest=[{'path':str(p.relative_to(VAULT)).replace('\\','/'),'model':m['model'],'name':m['name']} for p,t,m in created]
(ROOT/'agents-created.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=True,indent=2))
