// Project creation skills UI logic
(function(){
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("skills-container");
    if (!container) return;

    const isEdit = container.dataset.projectId !== "0";
    const addBtn = document.getElementById("add-skill-btn");
    const inputWrapper = document.getElementById("skill-input-wrapper");
    const input = document.getElementById("skill-input");
    const suggestions = document.getElementById("skill-suggestions");

    if (!addBtn || !inputWrapper || !input || !suggestions) return;

    // Temporary storage for skills during project creation
    const tempSkills = new Set();

    addBtn.addEventListener("click", () => {
      addBtn.classList.add("hidden");
      inputWrapper.classList.remove("hidden");
      input.value = "";
      suggestions.innerHTML = "";
      suggestions.classList.add("hidden");
      input.focus();
    });

    let timeout = null;
    input.addEventListener("input", () => {
      const q = input.value.trim();
      clearTimeout(timeout);
      if (!q) {
        suggestions.classList.add("hidden");
        suggestions.innerHTML = "";
        return;
      }
      timeout = setTimeout(async () => {
        try {
          const res = await fetch(`/projects/skills/?q=${encodeURIComponent(q)}`);
          if (!res.ok) return;

          const data = await res.json();
          suggestions.innerHTML = "";

          data.forEach(s => {
            const li = document.createElement("li");
            li.textContent = s.name;
            li.dataset.id = s.id;
            li.className = "suggestion-item";
            suggestions.appendChild(li);
          });

          const exact = data.some(s => s.name.toLowerCase() === q.toLowerCase());
          if (!exact) {
            const liNew = document.createElement("li");
            liNew.textContent = `Создать «${q}»`;
            liNew.dataset.name = q;
            liNew.className = "create-new";
            suggestions.appendChild(liNew);
          }

          suggestions.classList.remove("hidden");
        } catch (error) {
          console.error("Error fetching skills:", error);
        }
      }, 200);
    });

    suggestions.addEventListener("mousedown", async (e) => {
      const li = e.target.closest("li");
      if (!li) return;

      if (li.classList.contains("create-new")) {
        addSkillByName(li.dataset.name);
      } else if (li.dataset.id) {
        addSkillById(li.dataset.id);
      }
      hideInput();
    });

    input.addEventListener("keydown", async (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const q = input.value.trim();
        if (!q) return;

        const first = suggestions.querySelector("li");
        if (first && first.dataset.id) {
          await addSkillById(first.dataset.id);
        } else {
          await addSkillByName(q);
        }
        hideInput();
      }
      if (e.key === "Escape") {
        hideInput();
      }
    });

    input.addEventListener("blur", () => setTimeout(hideInput, 120));

    function hideInput() {
      inputWrapper.classList.add("hidden");
      suggestions.classList.add("hidden");
      addBtn.classList.remove("hidden");
    }

    container.addEventListener("click", async (e) => {
      if (e.target.classList.contains("remove-skill-btn")) {
        const chip = e.target.closest(".skill-chip");
        const skillName = chip.textContent.replace('×', '').trim();
        chip.remove();

        // Remove from temporary storage
        tempSkills.delete(skillName);

        // Update session storage for project creation
        if (!isEdit) {
          try {
            const response = await fetch('/save-temp-skills/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie("csrftoken"),
              },
              body: JSON.stringify({ skills: Array.from(tempSkills) }),
            });
          } catch (error) {
            console.error("Error saving temporary skills:", error);
          }
        }
      }
    });

    async function addSkillById(skillId) {
      try {
        // Make API call to add skill to project
        const projectId = container.dataset.projectId;

        let res;
        if (projectId === "0") {
          // For project creation, use GET request with skill_id parameter
          res = await fetch(`/projects/0/skills/add/?skill_id=${skillId}`, {
            method: "GET",
            headers: {
              "X-CSRFToken": getCookie("csrftoken"),
            },
          });
        } else {
          // For existing projects, use POST request
          res = await fetch(`/projects/${projectId}/skills/add/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ skill_id: skillId }),
          });
        }

        if (res.ok) {
          const skill = await res.json();
          appendChip(skill.id, skill.name);
          tempSkills.add(skill.name);

          // Update session storage for project creation
          if (!isEdit) {
            try {
              const response = await fetch('/save-temp-skills/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie("csrftoken"),
                },
                body: JSON.stringify({ skills: Array.from(tempSkills) }),
              });
            } catch (error) {
              console.error("Error saving temporary skills:", error);
            }
          }
        }
      } catch (error) {
        console.error("Error adding skill by ID:", error);
      }
    }
    async function addSkillByName(name) {
      appendChip(0, name);
      tempSkills.add(name);

      // Update session storage for project creation
      if (!isEdit) {
        try {
          const response = await fetch('/save-temp-skills/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie("csrftoken"),
            },
            body: JSON.stringify({ skills: Array.from(tempSkills) }),
          });
        } catch (error) {
          console.error("Error saving temporary skills:", error);
        }
      }
    }

    function appendChip(id, name) {
      if (Array.from(container.querySelectorAll(".skill-chip")).some(chip => chip.textContent.includes(name))) {
        return;
      }

      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.dataset.id = id;
      chip.innerHTML = `${name} <button type="button" class="remove-skill-btn" aria-label="Удалить" title="Удалить">×</button>`;

      container.insertBefore(chip, addBtn);

      const empty = container.querySelector(".skill-empty");
      if (empty) empty.remove();
    }

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
})();