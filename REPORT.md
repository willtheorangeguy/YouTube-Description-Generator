Run started:2026-07-09 03:43:21.330868+00:00

Test results:
>> Issue: [B615:huggingface_unsafe_download] Unsafe Hugging Face Hub download without revision pinning in from_pretrained()
   Severity: Medium   Confidence: High
   CWE: CWE-494 (https://cwe.mitre.org/data/definitions/494.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b615_huggingface_unsafe_download.html
   Location: .\src\youtube_description_generator\describe_frames.py:22:21
21	        _device = "cuda" if torch.cuda.is_available() else "cpu"
22	        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
23	        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(_device)

--------------------------------------------------
>> Issue: [B615:huggingface_unsafe_download] Unsafe Hugging Face Hub download without revision pinning in from_pretrained()
   Severity: Medium   Confidence: High
   CWE: CWE-494 (https://cwe.mitre.org/data/definitions/494.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b615_huggingface_unsafe_download.html
   Location: .\src\youtube_description_generator\describe_frames.py:23:17
22	        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
23	        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(_device)
24	    return _processor, _model, _device

--------------------------------------------------
>> Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b404-import-subprocess
   Location: .\src\youtube_description_generator\summarize_descriptions.py:4:0
3	from pathlib import Path
4	import subprocess
5	

--------------------------------------------------
>> Issue: [B607:start_process_with_partial_path] Starting a process with a partial executable path
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b607_start_process_with_partial_path.html
   Location: .\src\youtube_description_generator\summarize_descriptions.py:25:13
24	    # Use Ollama (assumes model is already pulled)
25	    result = subprocess.run(
26	        ["ollama", "run", "llama3.1:8b"],
27	        input=prompt.encode("utf-8"),
28	        capture_output=True,
29	    )
30	

--------------------------------------------------
>> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b603_subprocess_without_shell_equals_true.html
   Location: .\src\youtube_description_generator\summarize_descriptions.py:25:13
24	    # Use Ollama (assumes model is already pulled)
25	    result = subprocess.run(
26	        ["ollama", "run", "llama3.1:8b"],
27	        input=prompt.encode("utf-8"),
28	        capture_output=True,
29	    )
30	

--------------------------------------------------

Code scanned:
	Total lines of code: 489
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 3
		Medium: 2
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 0
		High: 5
Files skipped (0):
