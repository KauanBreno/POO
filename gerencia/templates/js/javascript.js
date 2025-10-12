document.addEventListener('DOMContentLoaded', function() {
  const razaoSocialInput = document.getElementById('id_razao_social');
  const nomeFantasiaInput = document.getElementById('id_nome_fantasia');
  const complementoInput = document.getElementById('id_endereco-0-complemento');
  const logradouroInput = document.getElementById('id_endereco-0-logradoro');
  const bairroInput = document.getElementById('id_endereco-0-bairro');
  const municipioInput = document.getElementById('id_endereco-0-municipio');
  const emailInput = document.getElementById('id_contatos-0-email');
  const urlInput = document.getElementById('id_contatos-0-url');
  const cnpjInput = document.getElementById('id_cnpj');
  const cepInput = document.getElementById('id_endereco-0-cep');
  const ufInput = document.getElementById('id_endereco-0-uf');
  const telInput = document.getElementById('id_contatos-0-telefone');
  const celInput = document.getElementById('id_contatos-0-celular');
  const whatsappCheck = document.getElementById('id_contatos-0-whatsapp');
  const insEstatualInput = document.getElementById('id_inscricao_estadual');
  const insMunicipalInput = document.getElementById('id_inscricao_municipal');
  Campos_genericos = [razaoSocialInput, nomeFantasiaInput, complementoInput, logradouroInput, bairroInput, municipioInput, emailInput, urlInput]

  celInput.addEventListener('change', function() {
    if (whatsappCheck.checked == true) {
      celInput.setAttribute('required', 'required');
    } else {
      whatsappCheck.checked = false;
      celInput.removeAttribute('required');
    }
  });

  function basicValition(valor) {
    let value = valor.trim()
    value = value.replace(/\s{2,}/g, ' ');
    return value
  }

  function cnpjMask(cnpj) {
    let value =  cnpj.replace(/\D/g, '');
    value = value.replace(/^(\d{2})(\d)/, '$1.$2');
    value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
    value = value.replace(/(\d{4})(\d)/, '$1-$2');
    return value.slice(0, 18);
  }

  function cepMask(cep) {
    let value = cep.replace(/\D/g, '');
    value = value.replace(/^(\d{5})(\d)/, '$1-$2')
    return value.slice(0, 9);
  }

  function telefoneMask (telefone) {
    let value = telefone.replace(/\D/g, '');
    value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
    value = value.replace(/(\d{4})(\d)/, '$1-$2');
    return value.slice(0, 15);
  }

  function celularMask (celular) {
    let value = celular.replace(/\D/g, '');
    value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    return value.slice(0, 15);
  }

  function ufMask (uf) {
    let value = uf.replace(/[^a-zA-Z]/g, '');
    return value.toUpperCase().slice(0, 2);
  }

  for (const campo of Campos_genericos) {
    if (campo) {
      campo.addEventListener('blur', function(e) {
        e.target.value = basicValition(e.target.value)
      })
    }
  }

  if (cnpjInput) {
    cnpjInput.addEventListener('input', function(e) {
      e.target.value = cnpjMask(e.target.value)
    });
  }

  if (cepInput) {
    cepInput.addEventListener('input', function(e) {
      e.target.value = cepMask(e.target.value)
    });
  }

  if (telInput) {
    telInput.addEventListener('input', function(e) {
      e.target.value = telefoneMask(e.target.value)
    });
  }

  if (celInput) {
    celInput.addEventListener('input', function(e) {
      e.target.value = celularMask(e.target.value)
    });
  }

  if (ufInput) {
    ufInput.addEventListener('input', function(e) {
      e.target.value = ufMask(e.target.value)
    });
  }

  if (whatsappCheck) {
    whatsappCheck.addEventListener('change', function() {
      if (this.checked) {
        celInput.setAttribute('required', 'required');
      } else {
        celInput.removeAttribute('required');
      }
    });
  }

  if (insEstatualInput) {
    insEstatualInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      e.target.value = value.slice(0, 30);
    });
  }

  if (insMunicipalInput) {
    insMunicipalInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      e.target.value = value.slice(0, 30);
    });
  }

  if (cnpjInput) {
    cnpjInput.addEventListener('blur', function(e) {
      const cnpj = event.target.value.replace(/\D/g, '');
      if (cnpj.length !== 14) {
        console.log('CNPJ inválido.');
        return;
      }

      const url = `https://brasilapi.com.br/api/cnpj/v1/${cnpj}`;

      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Erro ao consultar o CNPJ. Verifique se ele é válido.');
          }
          return response.json();
        })
        .then(data => {
          razaoSocialInput.value = data.razao_social;
          nomeFantasiaInput.value = data.nome_fantasia;
          logradouroInput.value = data.logradouro
          bairroInput.value = data.bairro
          municipioInput.value = data.municipio

          if (data.complemento) {
            complementoInput.value = data.complemento
          }
          if (data.cep) {
            cepInput.value = data.cep;
            cepInput.value = cepMask(cepInput.value)
          }
          if (data.uf) {
            ufInput.value = data.uf
            ufInput.value = ufMask(ufInput.value)
          }

          if (data.ddd_telefone_1) {
            telInput.value = data.ddd_telefone_1
            telInput.value = telefoneMask(telInput.value)
          }

          if (data.email) {
            emailInput.value = data.email
          }

          for (campo of Campos_genericos) {
            campa.value = basicValition(campo)
          }
        })
    })
  }

  if (cepInput) {
    cepInput.addEventListener('blur', function(e) {
      const cep = event.target.value.replace(/\D/g, '');
      if (cep.length !== 8) {
        console.log('CEP inválido.');
        return;
      }

      const url = `https://brasilapi.com.br/api/cep/v1/${cep}`;

      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Erro ao consultar o CEP. Verifique se ele é válido.');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          logradouroInput.value = data.street
          bairroInput.value = data.neighborhood
          municipioInput.value = data.city

          if (data.state) {
            ufInput.value = data.state
            ufInput.value = ufMask(ufInput.value)
          }
        })
    })
  }
});