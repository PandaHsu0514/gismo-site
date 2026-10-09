---json
{
 "title": "AI 秀出推理過程，能促進永續消費嗎",
 "date": "2026-05-27",
 "summary": "作者要處理的核心問題是：當對話式 AI 從「只給答案」的黑箱系統，變成會顯示推理過程的玻璃箱系統時，這種 reasoning transparency 到底會如何改變使用者感受與後續行為。更具體地…",
 "paperTitle": "Opening the black box: How reasoning-enabled AI agents influence user perceptions and behavior in sustainable consumption",
 "authors": "Pejman Ebrahimi, Stefan Hoffmann, Johannes Schneider",
 "year": "2026",
 "journal": "International Journal of Information Management, 90, 103075",
 "doi": "10.1016/j.ijinfomgt.2026.103075",
 "category": "管理",
 "card": "/files/notes/2026-05-27-opening-black-box-reasoning-enabled-ai.jpg"
}
---

## 1. 基本資訊

這篇文章由 Pejman Ebrahimi、Stefan Hoffmann 與 Johannes Schneider 發表於 2026 年的 *International Journal of Information Management*，題目為〈Opening the black box: How reasoning-enabled AI agents influence user perceptions and behavior in sustainable consumption〉，DOI 為 10.1016/j.ijinfomgt.2026.103075。文章把 CoT 從純技術議題轉成使用者層級的資訊管理問題，關心的不是模型推理是否更準，而是使用者看見推理鏈之後，是否更信任、更理解，也更願意採取行動。

## 2. 研究問題

作者要處理的核心問題是：當對話式 AI 從「只給答案」的黑箱系統，變成會顯示推理過程的玻璃箱系統時，這種 reasoning transparency 到底會如何改變使用者感受與後續行為。更具體地說，CoT 會不會讓使用者覺得更有幫助、更可信、更個人化，進而提高知識獲得與可持續消費行為意圖；還是說它反而會因資訊量增加、資料處理更可見而提高認知負荷與隱私疑慮。這個問題的重要性在於，它把 explainability 從抽象規範主張，變成可驗證的機制問題。

## 3. 理論基礎

理論上，本文整合了多個框架。正向機制主要借用 Technology Acceptance Model 與 IS Success Model，認為 reasoning transparency 能提升 perceived usefulness、trust、personalization 與 transparency，進而改善使用者結果。負向機制則引入 Cognitive Load Theory 與 Privacy Calculus Theory，指出過多推理步驟可能增加理解成本，也可能因揭露系統如何使用個人資訊而激發隱私顧慮。作者的關鍵理論張力不是「透明一定更好」，而是透明可能同時帶來促進與抑制兩種力量，最後要看哪一側更強。

## 4. 研究架構

研究設計分成三個 phase。Phase 1 是技術開發：研究團隊先微調一個 reasoning-enabled chatbot，讓它能在 sustainable consumption 情境中產出較高品質的 CoT 回應。Phase 2 是主體實驗：以 between-subjects 設計比較 CoT chatbot 與一般 chatbot，並透過一組促進與抑制中介變項來解釋它們對 perceived knowledge 與 behavioral intention 的影響。Phase 3 則做質性補強，蒐集使用者自由回饋，檢查他們實際如何感受這種 reasoning transparency。

## 5. 假設邏輯

作者把中介機制分成 promoters 與 inhibitors。H1 到 H5 主張 CoT chatbot 會透過提升 user-friendliness、usefulness、personalized information、trust 與 transparency，間接提高 perceived knowledge 與 behavioral intention。H6 到 H8 則檢驗另一條路：如果 CoT 減少 cognitive load、inefficiency 與 privacy concerns，那麼也會進一步提升兩項結果變數。這個假設邏輯很完整，因為它不只預設 CoT 有益，而是把「為什麼有益」與「可能為何有害」一起納進模型。

## 6. 方法

Phase 1 以 Qwen-2.5-3B-Instruct 為基礎模型，透過多代理資料生成、GRPO 與 LoRA 進行 parameter-efficient fine-tuning，目標是讓模型在永續消費問題上輸出更結構化、可追蹤的推理鏈。Phase 2 為隨機分派的線上實驗，最終樣本為 417 人，受試者來自 IT 專業社群；所有人都需和 chatbot 至少互動三分鐘並提出至少三個問題。之後以 PLSc-SEM 檢驗模型。量測變項包含 user-friendliness、usefulness、personalized information、trust、transparency、cognitive load、inefficiency、privacy concerns，以及兩個結果變項 perceived knowledge 與 behavioral intention。Phase 3 則由 128 名參與者提供開放式回饋，進行歸納式質性分析。

## 7. 結果

整體結果相當強。首先，CoT chatbot 使用者的 perceived knowledge 與 behavioral intention 都顯著高於一般 chatbot；平均數上，perceived knowledge 約從 3.68 提高到 6.05，behavioral intention 約從 3.61 提高到 6.06，兩者的 t 檢定都高度顯著。結構模型也顯示全部假設獲得支持：CoT 顯著提升 user-friendliness、usefulness、personalization、trust 與 transparency，同時顯著降低 cognitive load、inefficiency 與 privacy concerns。這些中介再分別對知識與行為意圖產生顯著影響。模型解釋力也很高，perceived knowledge 的 R² 為 0.832，behavioral intention 的 R² 為 0.817。質性結果則補充說明，CoT chatbot 被更多人描述為推理更清楚、答案更有幫助，而且顯著減少「答案太長太亂」「回應含糊」與「技術設計不佳」等負面評價。

## 8. 理論貢獻

這篇最大的理論價值，是把 CoT 從演算法效能議題轉譯成使用者心理機制議題。第一，它提供經驗證據說明 reasoning transparency 的價值不只在 interpretability，而在於會具體改變 trust、perceived usefulness、personalization 與 transparency 等採用前置機制。第二，它挑戰「透明會增加負擔」的單向悲觀論，因為在這個研究裡，CoT 不是讓認知負荷更高，反而降低了 cognitive load、inefficiency 與 privacy concerns。第三，它示範了一個很可重用的中介框架，讓後續研究可以不只問 explainable AI 有沒有用，而是問它透過哪些 promoter / inhibitor 改變人機互動結果。

## 9. 實務意涵

對實務設計者來說，這篇的訊息很明確：在高不確定、價值衝突多、需要多重權衡的情境中，AI 不應只給建議，更應解釋建議怎麼來。CoT 式設計能提升使用者的理解、信任與採納意願，而且不一定會造成資訊過載，前提是推理呈現要清楚、結構化、和任務脈絡對齊。對永續消費以外的場景也是如此，例如醫療、財務規劃、政策溝通與教育輔助，都可把 reasoning-enabled agent 視為比一般問答 bot 更有潛力的 decision-support 形式。

## 10. 研究限制

限制仍然存在。第一，研究情境放在 sustainable consumption，雖然這是很合適的高複雜決策脈絡，但外推到其他任務仍需小心。第二，主實驗樣本來自 IT 專業社群，這群人對新技術的理解與容忍度可能高於一般使用者。第三，Phase 1 的技術細節雖然強，但主文最終還是以使用者主觀感受與意圖為主，沒有檢驗長期行為是否真的持續改變。第四，研究比較的是 CoT 與非 CoT 版本，但沒有細拆不同透明度呈現格式，例如更短的摘要推理、互動式展開或自適應說明。第五，作者雖然納入隱私顧慮，但研究結果是在這個任務與樣本下觀察到隱私疑慮下降，未必代表所有高敏感資料情境都會如此。

## 11. 對我研究的啟發

這篇對我很有啟發，因為它正好補上我最近主線裡一塊很關鍵的中介機制：AI 不只是提供內容，它也透過「怎麼表達推理」來改變人的認知處理方式。第一個延伸方向，是把這套 promoter / inhibitor 框架搬到 human-GenAI collaboration 與 knowledge creation 任務中，檢查 CoT、解釋層次與回應結構是否會改變我的知識搜尋廣度、洞察品質或創意產出。第二個方向，是把這篇和我已經讀過的 cognitive style 文獻接起來，問不同 cognitive style 的人是否對 reasoning transparency 反應不同，例如理性型可能更偏好顯性推理鏈，直覺型則可能更受簡化結構或 narrative reasoning 影響。第三個方向，是把 transparency 當成人機協作設計變項，而不是單純的倫理附加值，進一步研究它如何與 trust calibration、task stakes、autonomy preference 一起影響 collaboration quality。

## 12. 整體評價

我認為這篇是本輪很值得先讀的一篇，因為它同時有新技術性與高可重用理論性。它不是重複說「可解釋 AI 比較好」，而是用三階段設計把技術開發、實驗驗證與主觀經驗串成一條完整論證鏈。對我目前的研究脈絡來說，這篇最有價值的不是永續消費本身，而是它提供了一個乾淨的答案：AI 的推理呈現方式本身，就是人機協作結果的重要機制變項。若我後面要往 human-GenAI collaboration、knowledge creation 或 AI-mediated cognition 走，這篇很適合當作「reasoning transparency 會如何作用」的代表性橋梁文。
