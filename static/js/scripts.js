window.onload = () => {
    function uploadFile(e) {
        document.querySelector('label').textContent = 'Документ загружен';
        document.querySelector('.btn-my').classList.remove("btn-my-disabled");
        document.querySelector('.btn-my').disabled = false;
    }
    async function setForm(e) {
        e.target.classList.add('btn-my-disabled');
        e.target.disabled = true;
        document.querySelector('p').textContent = 'Идет создание формы ...';

        let response = await fetch('/setform', { method: 'POST' });
        let result = await response.json();
        if (result.ok) {
            e.target.classList.remove('btn-my-disabled');
            e.target.disabled = false;
            document.querySelector('p').textContent = 'Форма создана!';
        } else {
            document.querySelector('p').textContent = 'Ошибка при создании формы';
            e.target.classList.remove('btn-my-disabled');
            e.target.disabled = false;
        }
    }

    let element_file = document.querySelector('#file');
    if (element_file) element_file.addEventListener('change', uploadFile);

    let element_set_form = document.querySelector('#set-form');
    if (element_set_form) element_set_form.addEventListener('click', setForm);
}