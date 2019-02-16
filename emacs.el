(defun playmus()
  (shell-command "curl 127.0.0.1:5000/start"))

(defun stopmus()
  (shell-command "curl 127.0.0.1:5000/stop"))

(add-hook 'org-clock-in-hook #'playmus)
(add-hook 'org-clock-out-hook #'stopmus)
