document.addEventListener('DOMContentLoaded', () => {
    // User Dropdown toggle logic
    const avatar = document.getElementById('avatar-btn');
    if (avatar) {
        avatar.addEventListener('click', (e) => {
            e.preventDefault();
            const dropdown = document.getElementById('user-dropdown');
            if (dropdown) {
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }
        });
    }

    // Worksheet Dropdown toggle logic
    const worksheetBtn = document.getElementById('worksheet-dropdown-btn');
    if (worksheetBtn) {
        worksheetBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const dropdown = document.getElementById('worksheet-dropdown');
            if (dropdown) {
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }
        });
    }

    // Close dropdowns on click outside
    document.addEventListener('click', (e) => {
        const userDropdown = document.getElementById('user-dropdown');
        if (userDropdown && avatar && !avatar.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.style.display = 'none';
        }
        
        const worksheetDropdown = document.getElementById('worksheet-dropdown');
        if (worksheetDropdown && worksheetBtn && !worksheetBtn.contains(e.target) && !worksheetDropdown.contains(e.target)) {
            worksheetDropdown.style.display = 'none';
        }
    });

    // Worksheet logic
    const updateProgress = () => {
        let filledCount = 0;
        let totalItems = 4; // 3 text areas + 1 group of checkboxes

        const inputs = document.querySelectorAll('.worksheet-input');
        inputs.forEach(input => {
            if (input.value.trim() !== '') filledCount++;
        });

        const checkedBoxes = document.querySelectorAll('.feature-checkbox:checked');
        if (checkedBoxes.length > 0) filledCount++;

        const percent = Math.round((filledCount / totalItems) * 100);
        
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar && progressText) {
            progressBar.style.width = `${percent}%`;
            progressText.textContent = `${percent}%`;
        }
    };

    const inputs = document.querySelectorAll('.worksheet-input');
    if (inputs.length > 0) {
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                // Update character count
                const charCountSpan = input.nextElementSibling.querySelector('.char-count');
                if (charCountSpan) {
                    charCountSpan.textContent = input.value.length;
                }

                // Update prompt sidebar
                const targetId = input.getAttribute('data-target');
                const targetSpan = document.getElementById(targetId);
                if (targetSpan) {
                    if (input.value.trim() !== '') {
                        targetSpan.textContent = input.value;
                        targetSpan.style.color = '#ddd';
                    } else {
                        targetSpan.textContent = '(not answered yet)';
                        targetSpan.style.color = '#888';
                    }
                }

                updateProgress();
            });
        });
    }

    const updateCategoryPrompt = (category) => {
        const groupCheckboxes = document.querySelectorAll(`.feature-checkbox[data-category="${category}"]:checked`);
        const targetSpan = document.getElementById(`prompt-${category}`);
        if (targetSpan) {
            if (groupCheckboxes.length > 0) {
                const values = Array.from(groupCheckboxes).map(box => {
                    if (box.classList.contains('other-checkbox')) {
                        const otherInput = document.querySelector(`.other-input[data-category="${category}"]`);
                        return (otherInput && otherInput.value.trim() !== '') ? otherInput.value.trim() : 'Other';
                    }
                    return box.value;
                });
                
                if (category === 'pages') {
                    const contentPagesInput = document.getElementById('content-pages-input');
                    if (contentPagesInput && contentPagesInput.value.trim() !== '') {
                        const customPages = contentPagesInput.value.split(',').map(s => s.trim()).filter(s => s);
                        values.push(...customPages);
                    }
                }
                
                if (category === 'pages') {
                    targetSpan.textContent = values.length > 0 ? '- ' + values.join('\n- ') : '- [none selected]';
                } else {
                    targetSpan.textContent = values.join(', ');
                }
                targetSpan.style.color = '#ddd';
            } else {
                if (category === 'pages') {
                    const contentPagesInput = document.getElementById('content-pages-input');
                    if (contentPagesInput && contentPagesInput.value.trim() !== '') {
                        const customPages = contentPagesInput.value.split(',').map(s => s.trim()).filter(s => s);
                        targetSpan.textContent = '- ' + customPages.join('\n- ');
                        targetSpan.style.color = '#ddd';
                        return; // Exit early so we don't apply the 'none selected' styling below
                    }
                    targetSpan.textContent = '- [none selected]';
                } else {
                    targetSpan.textContent = '[none selected]';
                }
                targetSpan.style.color = '#888';
            }
        }
    };

    const checkboxes = document.querySelectorAll('.feature-checkbox');
    if (checkboxes.length > 0) {
        checkboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                const category = cb.getAttribute('data-category');
                if (cb.classList.contains('other-checkbox')) {
                    const input = document.querySelector(`.other-input[data-category="${category}"]`);
                    if (input) {
                        input.style.display = cb.checked ? 'block' : 'none';
                        if (!cb.checked) {
                            input.value = '';
                        }
                    }
                }
                updateCategoryPrompt(category);
                updateProgress();
            });
        });
    }

    const otherInputsList = document.querySelectorAll('.other-input');
    if (otherInputsList.length > 0) {
        otherInputsList.forEach(input => {
            input.addEventListener('input', () => {
                const category = input.getAttribute('data-category');
                updateCategoryPrompt(category);
            });
        });
    }

    const contentPagesInput = document.getElementById('content-pages-input');
    if (contentPagesInput) {
        contentPagesInput.addEventListener('input', () => {
            updateCategoryPrompt('pages');
            updateProgress();
        });
    }

    // Copy prompt logic
    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const promptOutput = document.getElementById('generated-prompt-output');
            if (promptOutput) {
                // Copy the rendered text exactly as it appears
                let textToCopy = promptOutput.innerText;
                
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
                    setTimeout(() => { copyBtn.innerHTML = originalText; }, 2000);
                });
            }
        });
    }

    // Save worksheet logic
    const saveBtn = document.getElementById('save-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const purpose = document.querySelector('[data-target="prompt-purpose"]')?.value || '';
            const target_user = document.querySelector('[data-target="prompt-user"]')?.value || '';
            const mission = document.querySelector('[data-target="prompt-mission"]')?.value || '';
            
            const getCheckedValues = (category) => {
                const values = Array.from(document.querySelectorAll(`.feature-checkbox[data-category="${category}"]:checked`)).map(cb => {
                    if (cb.classList.contains('other-checkbox')) {
                        const input = document.querySelector(`.other-input[data-category="${category}"]`);
                        return (input && input.value.trim() !== '') ? input.value.trim() : 'Other';
                    }
                    return cb.value;
                });
                
                if (category === 'pages') {
                    const contentPagesInput = document.getElementById('content-pages-input');
                    if (contentPagesInput && contentPagesInput.value.trim() !== '') {
                        const customPages = contentPagesInput.value.split(',').map(s => s.trim()).filter(s => s);
                        values.push(...customPages);
                    }
                }
                
                return values;
            };
            
            const nav_features = getCheckedValues('nav');
            const auth_features = getCheckedValues('auth');
            const footer_features = getCheckedValues('footer');
            const pages = getCheckedValues('pages');
            
            const promptOutput = document.getElementById('generated-prompt-output');
            let generated_prompt = promptOutput ? promptOutput.innerText : '';
            
            const originalText = saveBtn.textContent;
            saveBtn.textContent = 'Saving...';
            saveBtn.disabled = true;
            
            fetch('/api/worksheets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    purpose, target_user, mission, nav_features, auth_features, footer_features, pages, generated_prompt
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    saveBtn.textContent = 'Saved successfully!';
                    setTimeout(() => {
                        window.location.href = '/worksheet/history';
                    }, 1000);
                } else {
                    alert('Error saving worksheet: ' + data.error);
                    saveBtn.textContent = originalText;
                    saveBtn.disabled = false;
                }
            })
            .catch(err => {
                console.error(err);
                alert('Error saving worksheet');
                saveBtn.textContent = originalText;
                saveBtn.disabled = false;
            });
        });
    }
});
