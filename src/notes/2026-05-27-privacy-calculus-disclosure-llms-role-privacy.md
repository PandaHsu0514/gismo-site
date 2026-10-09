---json
{
 "title": "使用大型語言模型時，人們願意透露多少隱私",
 "date": "2026-05-27",
 "summary": "本文的核心問題可以濃縮成兩個。第一，privacy controls、privacy by design、privacy nudges 與 anthropomorphic HCI 是否會提高使用者…",
 "paperTitle": "Privacy calculus and disclosure in LLMs: The role of privacy controls, nudges, and perceived anthropomorphism",
 "authors": "Shantanu Dey, Saurabh Kumar",
 "year": "2026",
 "journal": "International Journal of Information Management, 89, 103071",
 "doi": "10.1016/j.ijinfomgt.2026.103071",
 "category": "管理",
 "card": "/files/notes/2026-05-27-privacy-calculus-disclosure-llms-role-privacy.jpg"
}
---

## 1. 基本資訊

這篇文章由 Shantanu Dey 與 Saurabh Kumar 發表於 2026 年的 International Journal of Information Management，題目是〈Privacy calculus and disclosure in LLMs: The role of privacy controls, nudges, and perceived anthropomorphism〉，DOI 為 10.1016/j.ijinfomgt.2026.103071。文章要處理的是：當人和 anthropomorphic 的 LLM 代理互動時，為什麼有些人願意揭露更多資訊，而這個過程裡 privacy guardrails 到底怎麼發揮作用。

## 2. 研究問題

本文的核心問題可以濃縮成兩個。第一，privacy controls、privacy by design、privacy nudges 與 anthropomorphic HCI 是否會提高使用者對 LLM 代理的 disclosure willingness。第二，這些因素是透過什麼路徑運作，也就是它們如何改變 privacy concerns、perceived risk、perceived value 與資訊邊界管理。作者關心的不是單一瞬間的 disclosure，而是 LLM 持續對話與跨 session 記憶下，資訊邊界如何被逐步推移。

## 3. 理論基礎

理論上，本文結合了 communication privacy management（CPM）與 privacy calculus。CPM 強調人會透過 privacy rules 管理私人資訊的邊界，並在資訊分享後形成 co-ownership 與 boundary turbulence 的風險。Privacy calculus 則強調使用者會在 perceived risk 與 perceived value 之間做權衡，決定是否揭露資訊。作者把這兩套理論接到 LLM 情境，指出 anthropomorphic 對話與持續記憶會讓 disclosure 不再是單次交易，而是動態、跨回合的 boundary shift。

## 4. 研究架構

整體模型把 sensitive information context、privacy control、privacy by design、privacy nudges 與 anthropomorphic human-computer interaction 放進同一套路徑裡。Sensitive information 會提高 privacy concerns，privacy concerns 進一步提高 perceived risk，而 perceived risk 會壓低 willingness to disclose。另一方面，privacy by design 與 privacy nudges 會透過 trustful、human-like 的互動提升 perceived anthropomorphism，進一步提高 perceived value，而 perceived value 會推動 disclosure intention。作者把這個過程解釋成一種從個人所有權走向資訊共擁的邊界移動。

## 5. 假設邏輯

主要假設包含幾條路徑。H1 認為 privacy concerns 會提高 perceived risk；H2 認為 user-driven privacy control settings 會降低 privacy concerns；H3A 與 H3B 認為若系統揭露 privacy-by-design features，會提升 privacy control 感與對 anthropomorphic HCI 的信任；H4 認為 privacy nudges 會提升 anthropomorphic HCI 的信任知覺；H5 認為 anthropomorphic HCI 會提高 perceived value；H6 認為 perceived risk 會降低 disclosure willingness；H7 認為 perceived value 會提高 willingness to disclose；H8 則認為資訊敏感度會提高 privacy concerns。作者的邏輯很清楚：風險與價值分別透過不同設計機制被放大或緩和。

## 6. 方法

研究使用 scenario-based survey 與 PLS-SEM。作者先做 pilot 與 pre-test，之後正式蒐集約 230 份有效樣本，受試者來自 Prolific，並要求具備隱私意識且熟悉 chatGPT、Gemini 或 Bing 等 conversational AI。研究用 vignette 操弄不同情境，包括隱私設定、privacy nudges、privacy-by-design 保證與 anthropomorphic agent 互動，再以五點量表衡量 privacy concerns、perceived risk、perceived value、privacy controls、privacy by design、privacy nudges、anthropomorphic HCI 與 willingness to disclose。分析上以 PLS-SEM 為主，並檢驗信效度、CMV、效應量與不同隱私群組的比較。

## 7. 結果

結果大致支持整體模型。Privacy concerns 顯著提高 perceived risk，而 perceived risk 顯著降低 willingness to disclose。Sensitive information context 也明顯提高 privacy concerns。另一方面，privacy by design 強烈提升 privacy control 與 anthropomorphic HCI 的信任知覺；privacy nudges 也顯著提升 anthropomorphic HCI。Anthropomorphic HCI 再顯著提高 perceived value，而 perceived value 對 willingness to disclose 有明顯正向效果。比較有意思的是，privacy control 雖然對 privacy concerns 有負向效果，但效果相對弱，顯示在 LLM 這種動態對話脈絡裡，單純讓使用者自己切設定，不如 privacy assurance 與 trustful interaction 來得關鍵。

## 8. 理論貢獻

這篇最大的理論價值，是把傳統多用於 episodic transaction 的 privacy calculus，延伸到 LLM 這種持續互動、跨回合記憶的情境。第一，它把 CPM 的 information co-ownership 與 boundary permeability 概念帶進 anthropomorphic AI agent，說明人和 AI 的互動會逐步重寫「誰擁有這些資訊」。第二，它指出 disclosure 不只是 risk-benefit 的靜態權衡，而是會受 nudges、design assurance 與 human-like trust cues 動態塑形。第三，它給出一個很可重用的觀點：在生成式 AI 情境裡，privacy 問題不能只當治理議題，而要當作 interaction design 與 cognition 問題一起看。

## 9. 實務意涵

對產品與服務設計者來說，這篇很務實。若希望使用者願意分享資訊，不該只靠預設隱私設定，而要把 privacy-by-design、顯性 privacy controls、及時 nudges 與人性化訊息框架一起設計進去。換句話說，提升 disclosure willingness 的有效做法，不是單純讓 AI 更會說話，而是讓人感覺自己仍有邊界控制，同時又相信系統有制度性保護。對 direct-to-consumer 與服務業的 LLM agent 設計尤其重要，因為 personalization 與 privacy 之間的張力會直接影響後續互動深度。

## 10. 研究限制

限制主要有幾個。第一，研究基於 scenario-based survey，而不是直接觀察真實 LLM 互動行為，因此外部效度仍有限。第二，樣本來自 Prolific 的英文使用者，文化與語境相對集中。第三，作者雖然處理了不同 privacy setting 群組，但關於長期 disclosure 軌跡與實際 boundary turbulence，仍缺少縱貫資料。第四，anthropomorphism 在模型裡偏向 trust cue，而沒有再細拆成更具體的語氣、記憶、角色設定或情感表達形式。

## 11. 對我研究的啟發

這篇對我很有用，因為它把人機協作裡另一條常被低估的主線補上了：資訊揭露與邊界管理。第一個可直接延伸方向，是把這套 privacy calculus × CPM 框架搬進 human-GenAI collaboration 任務中，去看 knowledge seeking 或創意協作時，我是否也會因 anthropomorphic cue 而逐步鬆動自己的 disclosure boundary。第二個方向，是把這篇和我前面讀過的 anthropomorphism、empathy、autonomy、dependency 文獻接起來，研究「像人」的 AI 是否一方面提升價值感，一方面也提高過度依賴與資訊外洩風險。第三個方向，是把 cognitive style 或 AI literacy 帶進來，檢查不同類型的人在 nudges、privacy controls 與 perceived value 之間是否存在不同的權衡模式。

## 12. 整體評價

我認為這篇是 backlog 裡很值得優先讀的一篇，因為它不是只做一篇泛泛的隱私研究，而是真的抓到 LLM 時代特有的問題：對話式、記憶式、擬人化的 AI 會讓 disclosure 變成一個動態邊界問題。文章的強項是理論整合得不錯，把 privacy calculus 與 CPM 自然接在一起，而且對產品設計也有直接含義。若要挑剔，就是它目前仍偏 scenario 與自陳意圖層次，還沒有真的追到長期行為後果；但作為我未來串接 trust、anthropomorphism、dependency 與 knowledge disclosure 的橋梁文，這篇很夠力。
