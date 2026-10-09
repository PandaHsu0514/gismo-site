---json
{
 "title": "AI 輔助績效考核的錨定偏誤",
 "date": "2026-05-27",
 "summary": "作者要回答三個層次的問題。第一，AI 推薦數值是否會在績效考核中產生明顯 anchoring effect。第二，當同樣的高錨或低錨來自 AI 而不是人類時，管理者是否會更靠近 AI 的建議。第三…",
 "paperTitle": "How was my performance? Exploring the role of anchoring bias in AI-assisted decision making",
 "authors": "Lemuria Carter, Dapeng Liu",
 "year": "2025",
 "journal": "International Journal of Information Management, 82, 102875",
 "doi": "10.1016/j.ijinfomgt.2025.102875",
 "category": "管理",
 "card": "/files/notes/2026-05-27-was-my-performance-exploring-role-anchoring.jpg"
}
---

## 1. 基本資訊

這篇文章由 Lemuria Carter 與 Dapeng Liu 發表於 2025 年的 *International Journal of Information Management*，題目為〈How was my performance? Exploring the role of anchoring bias in AI-assisted decision making〉，DOI 為 10.1016/j.ijinfomgt.2025.102875。研究焦點放在 AI 輔助決策進入組織管理後，是否會像人類建議一樣成為錨點，甚至因為 AI 被視為更客觀而帶來更強的偏誤。整體設計採 mixed-methods，結合兩個控制實驗與一個 critical incident technique 的質性驗證。

## 2. 研究問題

作者要回答三個層次的問題。第一，AI 推薦數值是否會在績效考核中產生明顯 anchoring effect。第二，當同樣的高錨或低錨來自 AI 而不是人類時，管理者是否會更靠近 AI 的建議。第三，若確實存在 AI 錨定偏誤，低成本的去偏誤策略 CTO（consider-the-opposite）能否有效降低這種影響。這組問題的重要性在於，它把 AI 從「提供效率」的工具，轉成「會重塑判斷流程」的制度性因素來看。

## 3. 理論基礎

本文核心理論基礎是 anchoring and adjustment bias。依照 Tversky 與 Kahneman 的傳統觀點，決策者一旦先接收到某個初始數值，就會以它為參照進行不充分調整，最後判斷仍偏向初始錨點。作者把這套認知偏誤理論延伸到 AI-assisted decision making，主張 AI 建議之所以可能更危險，不是因為它一定比較錯，而是因為人會把它視為 data-driven、情緒較少、相對客觀，因此更容易放下警戒。去偏誤部分則引入 consider-the-opposite，認為要求決策者主動思考「為什麼這個建議可能太高／太低」可以打破原本被錨點固定的認知框架。

## 4. 研究架構

研究架構很清楚，可分成三段。第一段比較高錨與低錨是否在非 AI 情境下重現既有 anchoring effect。第二段把錨點來源改成 AI，檢驗 AI recommendation 是否同樣造成錨定，並比較 AI 與非 AI 在高錨與低錨條件下的差異。第三段只保留 AI 情境，再加入 CTO 干預，觀察去偏誤是否能把評分拉離 AI 錨點。最後再用 CIT 訪談式回溯法確認實驗發現是否和真實世界的 AI 使用經驗一致。

## 5. 假設邏輯

這篇是標準假設檢驗研究。H1 預期在非 AI 情境中，高錨組的績效評分會顯著高於低錨組，作為既有研究的 replication。H2 預期在 AI 情境中，高錨 AI 組評分也會顯著高於低錨 AI 組，證明 AI recommendation 會形成 anchoring effect。H3a 與 H3b 進一步比較 AI 與非 AI 錨點來源，作者預期高錨 AI 組會比高錨非 AI 組更靠近錨點，低錨 AI 組也會比低錨非 AI 組更靠近錨點，理由是 AI 被視為更客觀。H4a 與 H4b 則檢驗 CTO 去偏誤效果，預期在 AI 高錨情境下，接受 CTO 的受試者會給出較低分數；在 AI 低錨情境下，接受 CTO 的受試者會給出較高分數。

## 6. 方法

研究共分三個 study。Study 1 採 2（AI vs. human recommendation）× 2（high vs. low anchor）控制實驗，讓具 supervisory experience 的美國受試者扮演主管，根據 vignette 評估部屬績效。研究者在 2022 年 4 月透過 Prolific 招募樣本，423 人中有 377 份有效回覆。高錨條件提供前一年評分 91/100，低錨條件提供較低評分，觀察最後績效評分差異。Study 2 延伸為 AI-only 的 2（CTO vs. non-CTO）× 2（high vs. low anchor）設計，共 439 人、398 份有效回覆；CTO 操作要求受試者列出兩個「為何這個錨點可能不適當」的理由。Study 3 則以有管理經驗者進行 CIT 線上蒐集，45 份回覆中保留 24 份有效個案，用來檢查真實世界中 AI 數值建議與去偏誤經驗。

## 7. 結果

Study 1 先成功重現非 AI 錨定偏誤，支持 H1。AI 條件下也出現強烈錨定，高錨 AI 組平均評分 89.64，低錨 AI 組為 72.66，差異顯著，支持 H2。來源比較方面，H3a 獲支持：高錨 AI 組的評分比高錨非 AI 組更靠近錨點，顯示高分 AI 建議的錨定力更強；但 H3b 不成立，低錨 AI 與低錨非 AI 並無顯著差異，表示 AI 的放大效果主要出現在高錨而非低錨情境。Study 2 顯示 CTO 對高錨 AI 有效，CTO 高錨組平均 84.64，顯著低於未介入高錨組的 90.58，支持 H4a；但低錨條件下 CTO 未顯著提高評分，H4b 不成立。Study 3 的 CIT 也大致呼應前述結論：23/24 位受試者曾依賴 AI 數值建議，11 人有使用 CTO 經驗，其中 10 人認為 CTO 有幫助，顯示真實情境中也存在 AI 錨點與去偏誤需求。

## 8. 理論貢獻

這篇最重要的理論貢獻，是把傳統 cognitive bias 研究具體帶入 AI-assisted organizational decision making。第一，它提供了相當直接的證據說明 AI recommendation 不是中性的資訊輸入，而是可能因為「被認為較客觀」而變成更強的錨點。第二，它把 anchoring bias 從一般判斷研究，推進到績效考核這種具制度後果的管理場景，讓認知偏誤研究更貼近實務。第三，它證明 consider-the-opposite 這種低成本機制至少對高錨 AI 有效，為後續研究 AI governance、decision support interface design 與 debiasing workflow 提供可操作起點。

## 9. 實務意涵

對組織來說，這篇的訊息相當直接：把 AI 接進績效考核、選才、醫療或金融等高風險判斷流程，不代表偏誤自然減少，反而可能因為使用者過度信任 AI 而放大偏誤。管理者不能把 AI 分數當作「比較客觀的第一答案」，而應視為需要交叉檢驗的參考訊號。作者也提供一個很務實的方向，就是把 CTO 或類似反思提示嵌進系統介面，例如在主管送出最終評分前，要求他回答為何 AI 建議可能過高或過低。這類介面設計比單純做 bias training 更容易進入日常流程。

## 10. 研究限制

限制也很清楚。第一，研究採線上控制實驗與 vignette，雖然內部效度高，但和真實績效考核中的資訊量、政治因素與長期關係相比仍然簡化。第二，樣本主要是美國具管理經驗的 Prolific 受試者，外推到其他文化與制度情境要保守。第三，研究只處理 anchoring bias，尚未檢驗 confirmation bias、overconfidence 或 availability bias 等其他常見 AI-assisted decision bias。第四，作者比較的是 AI 與一種人類來源建議，沒有細拆不同 human source 的差異。第五，文中也承認目前尚缺統一量表去衡量 AI-related anchoring bias 強度，因此跨研究比較仍有限。

## 11. 對我研究的啟發

這篇對我很有用，因為它把人機協作的問題從「創造性知識產出」往前推到「人在接收 AI 建議時到底怎麼判斷」。如果我後續要研究 human-GenAI collaboration 與 knowledge creation，這篇提醒我不能只看最後成果品質，也要看中間是否有某些認知機制讓人過度依賴 AI。第一個可延伸方向，是把這種 anchoring 邏輯搬到創意任務或知識搜尋任務，檢查 AI 初始建議是否會限制人類後續探索廣度，反而傷害 novelty。第二個方向，是把我最近累積的 cognitive style 主線接上來，問理性型與直覺型我是否對 AI 錨點的敏感度不同。第三個方向，是把 CTO 類去偏誤設計轉成 knowledge creation workflow 的 prompt 或介面機制，例如要求我在採納 AI 觀點前先提出反例、替代框架或反向證據。

## 12. 整體評價

我認為這篇很適合放在本輪 backlog 優先讀，因為它不是泛泛談 AI adoption，而是精準處理「AI 建議如何改變管理判斷」這個更具機制感的問題。文章優點是研究問題清楚、實驗結構乾淨、對實務場景也有直接指向，而且高錨 AI 與去偏誤的非對稱結果很有啟發性。相較於我前幾輪讀的 collaboration / trust / task-fit 研究，這篇補上的不是另一個正向成效，而是一個很關鍵的風險機制。它未必直接回答 knowledge creation，但很適合作為我建立 human-GenAI collaboration 邊界條件與認知風險模型時的重要拼圖。
