(defun playmus()
  (shell-command "curl 127.0.0.1:5000/start"))

(defun stopmus()
  (interactive)
  (let* ((minutes  (string-to-number (subseq (org-clock-get-clock-string) 4 6)))
	 (hours    (* 60 (string-to-number (subseq (org-clock-get-clock-string) 2 3))))
	 (total    (number-to-string (+ hours minutes)))
	 (rating   (read-string "How focused where you from (1-5): "))
	 (comm     (concat "curl --data 'focus=" rating "&time=" total "' 127.0.0.1:5000/stop")))
    (shell-command comm)))

(add-hook 'org-clock-in-hook 'playmus)
(add-hook 'org-clock-out-hook 'stopmus)

