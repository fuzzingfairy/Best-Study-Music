(defun playmus()
  (shell-command "curl 127.0.0.1:5000/start"))

(defun stopmus()
  (interactive)
  (shell-command (concat "curl --data 'focus=" (read-string "How focused where you from (1-5): ") "' 127.0.0.1:5000/stop")))

(add-hook 'org-clock-in-hook #'playmus)
(add-hook 'org-clock-out-hook #'stopmus)

