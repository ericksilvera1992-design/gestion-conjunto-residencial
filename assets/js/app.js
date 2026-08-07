document.addEventListener('DOMContentLoaded',()=>{
  // Simple login redirect (placeholder)
  const loginForm=document.getElementById('loginForm');
  if(loginForm){
    loginForm.addEventListener('submit',(e)=>{e.preventDefault();window.location.href='dashboard.html'})
  }

  // Sidebar toggle for mobile and responsive
  const toggles=[...document.querySelectorAll('[id^=menuToggle]')];
  toggles.forEach(btn=>btn.addEventListener('click',e=>{
    e.stopPropagation();
    const sidebar=document.querySelector('.sidebar');
    sidebar?.classList.toggle('open');
  }));
  
  // Close sidebar when clicking outside
  document.addEventListener('click',()=>{
    const sidebar=document.querySelector('.sidebar');
    if(window.innerWidth<=768 && sidebar?.classList.contains('open')){
      sidebar.classList.remove('open');
    }
  });
  
  // Close sidebar when clicking on a link
  document.querySelectorAll('.sidebar a').forEach(link=>{
    link.addEventListener('click',()=>{
      const sidebar=document.querySelector('.sidebar');
      if(window.innerWidth<=768) sidebar?.classList.remove('open');
    });
  });

  // Populate dashboard counts (mock)
  if(document.getElementById('countResidents')){
    document.getElementById('countResidents').textContent=128
    document.getElementById('countVehicles').textContent=72
    document.getElementById('countReserves').textContent=14
    document.getElementById('countPayments').textContent=54
  }

  // Residents search and filter logic
  const searchRes=document.getElementById('searchResident');
  const filterType=document.getElementById('filterType');
  const filterStatus=document.getElementById('filterStatus');
  const resultsCount=document.getElementById('resultsCount');
  const residentCountTotal=document.getElementById('totalResidents');
  const ownersCount=document.getElementById('ownersCount');
  const rentersCount=document.getElementById('rentersCount');
  const delinquentCount=document.getElementById('delinquentCount');
  const residentModal=document.getElementById('residentModal');
  const addResidentBtn=document.getElementById('addResidentBtn');
  const closeResidentModal=document.getElementById('closeResidentModal');
  const cancelResidentBtn=document.getElementById('cancelResidentBtn');
  const residentForm=document.getElementById('residentForm');

  const getRows=()=>Array.from(document.querySelectorAll('#residentsTable tbody tr'));

  // Load residents from localStorage
  const loadResidents=()=>{
    const raw=localStorage.getItem('residentsTable');
    return raw?JSON.parse(raw):[];
  };

  // Save residents to localStorage
  const saveResidents=(residents)=>{
    localStorage.setItem('residentsTable',JSON.stringify(residents));
  };

  // Initialize with sample residents if empty
  if(loadResidents().length===0){
    saveResidents([
      {cedula:'1001234567',fullName:'Carlos Arango',phone:'3001234567',tower:'A',apartment:'101',residentType:'Propietario',status:'Activo'},
      {cedula:'1007654321',fullName:'María González',phone:'3007654321',tower:'A',apartment:'102',residentType:'Arrendatario',status:'Activo'},
      {cedula:'1009876543',fullName:'Juan Pérez',phone:'3009876543',tower:'B',apartment:'201',residentType:'Propietario',status:'Activo'},
      {cedula:'1005432109',fullName:'Sandra López',phone:'3005432109',tower:'B',apartment:'202',residentType:'Arrendatario',status:'Activo'},
      {cedula:'1002468135',fullName:'Roberto Silva',phone:'3002468135',tower:'C',apartment:'301',residentType:'Propietario',status:'Activo'},
      {cedula:'1003691359',fullName:'Catalina Ruiz',phone:'3003691359',tower:'A',apartment:'103',residentType:'Arrendatario',status:'Inactivo'},
      {cedula:'1004829567',fullName:'Fernando Torres',phone:'3004829567',tower:'C',apartment:'302',residentType:'Propietario',status:'Activo'},
      {cedula:'1008573924',fullName:'Valeria Moreno',phone:'3008573924',tower:'B',apartment:'203',residentType:'Arrendatario',status:'Activo'},
      {cedula:'1006429857',fullName:'Andrés Díaz',phone:'3006429857',tower:'D',apartment:'401',residentType:'Propietario',status:'Activo'},
      {cedula:'1009213456',fullName:'Lucía Martínez',phone:'3009213456',tower:'D',apartment:'402',residentType:'Arrendatario',status:'Inactivo'}
    ]);
  }

  // Render residents table
  const renderResidents=(residents)=>{
    const tbody=document.getElementById('residentsTableBody');
    if(!tbody) return;
    
    if(residents.length===0){
      tbody.innerHTML='<tr><td colspan="8" style="text-align:center;padding:40px;color:#999">Sin residentes aún</td></tr>';
      return;
    }
    
    tbody.innerHTML=residents.map(r=>`
      <tr>
        <td><strong>${r.cedula}</strong></td>
        <td><strong>${r.fullName}</strong></td>
        <td>${r.phone}</td>
        <td><strong>Torre ${r.tower}</strong></td>
        <td><strong>Apto ${r.apartment}</strong></td>
        <td><span class="badge badge-type">${r.residentType}</span></td>
        <td><span class="badge badge-status active">Activo</span></td>
        <td class="actions">
          <button class="action-btn edit-btn" data-id="${r.cedula}" title="Editar">✏️</button>
          <button class="action-btn delete-btn" data-id="${r.cedula}" title="Eliminar">🗑</button>
        </td>
      </tr>
    `).join('');

    // Delete handlers
    document.querySelectorAll('.delete-btn').forEach(btn=>{
      btn.addEventListener('click',e=>{
        const cedula=btn.dataset.id;
        if(confirm('¿Eliminar este residente?')){
          const updated=loadResidents().filter(r=>r.cedula!==cedula);
          saveResidents(updated);
          renderAndFilterResidents();
          updateResidentStats();
        }
      });
    });
  };

  const updateResidentStats=()=>{
    const residents=loadResidents();
    let owners=0;
    let renters=0;
    let delinquents=0;

    residents.forEach(r=>{
      if(r.residentType==='Propietario') owners++;
      if(r.residentType==='Arrendatario') renters++;
      if(r.status==='Inactivo') delinquents++;
    });

    if(residentCountTotal) residentCountTotal.textContent=residents.length;
    if(ownersCount) ownersCount.textContent=owners;
    if(rentersCount) rentersCount.textContent=renters;
    if(delinquentCount) delinquentCount.textContent=delinquents;
  };

  const filterAndSearchResidents=()=>{
    const residents=loadResidents();
    const query=searchRes?.value.toLowerCase()||'';
    const type=filterType?.value||'all';
    const status=filterStatus?.value||'all';

    const filtered=residents.filter(r=>{
      const matchesQuery=!query || 
        r.fullName.toLowerCase().includes(query) ||
        r.cedula.toLowerCase().includes(query) ||
        r.apartment.toLowerCase().includes(query) ||
        r.tower.toLowerCase().includes(query);
      
      const matchesType=type==='all' || r.residentType===type;
      const matchesStatus=status==='all' || (r.status||'Activo')===status;
      
      return matchesQuery && matchesType && matchesStatus;
    });

    renderResidents(filtered);
    if(resultsCount){
      resultsCount.textContent=`${filtered.length} resultado${filtered.length===1?'':'s'}`;
    }
  };

  const renderAndFilterResidents=()=>{
    filterAndSearchResidents();
  };

  const openResidentModal=()=>{
    residentForm?.reset();
    residentModal?.classList.remove('hidden');
  };

  const closeResidentModalWindow=()=>{
    residentForm?.reset();
    residentModal?.classList.add('hidden');
  };

  if(addResidentBtn){
    addResidentBtn.addEventListener('click',openResidentModal);
  }
  if(closeResidentModal){
    closeResidentModal.addEventListener('click',closeResidentModalWindow);
  }
  if(cancelResidentBtn){
    cancelResidentBtn.addEventListener('click',closeResidentModalWindow);
  }
  if(residentModal){
    residentModal.addEventListener('click',e=>{
      if(e.target===residentModal) closeResidentModalWindow();
    });
  }
  if(residentForm){
    residentForm.addEventListener('submit',e=>{
      e.preventDefault();
      const cedula=document.getElementById('cedula').value.trim();
      const fullName=document.getElementById('fullName').value.trim();
      const phone=document.getElementById('phone').value.trim();
      const tower=document.getElementById('tower').value.trim();
      const apartment=document.getElementById('apartment').value.trim();
      const residentType=document.getElementById('residentType').value;

      if(!cedula||!fullName||!phone||!tower||!apartment||!residentType) return;

      const residents=loadResidents();
      residents.push({cedula,fullName,phone,tower,apartment,residentType,status:'Activo'});
      saveResidents(residents);

      closeResidentModalWindow();
      renderAndFilterResidents();
      updateResidentStats();
    });
  }

  if(searchRes){
    searchRes.addEventListener('input',renderAndFilterResidents);
  }
  if(filterType){
    filterType.addEventListener('change',renderAndFilterResidents);
  }
  if(filterStatus){
    filterStatus.addEventListener('change',renderAndFilterResidents);
  }

  renderAndFilterResidents();
  updateResidentStats();

  // QR generator for visitas (new layout)
  const visitorName=document.getElementById('visitorName');
  const visitorDocument=document.getElementById('visitorDocument');
  const visitorList=document.getElementById('visitorList');
  const visitDate=document.getElementById('visitDate');
  const visitTime=document.getElementById('visitTime');
  const validMinutes=document.getElementById('validMinutes');
  const customMinutesRow=document.getElementById('customMinutesRow');
  const customMinutes=document.getElementById('customMinutes');
  const generateQrBtn=document.getElementById('generateQrBtn');
  const qrPreview=document.getElementById('qrPreview');
  const qrState=document.getElementById('qrState');
  const qrCreated=document.getElementById('qrCreated');
  const qrExpires=document.getElementById('qrExpires');
  const downloadQrBtn=document.getElementById('downloadQrBtn');
  const shareQrBtn=document.getElementById('shareQrBtn');
  const activeVisitsCount=document.getElementById('activeVisitsCount');
  const visitForm=document.getElementById('visitForm');
  const clearHistoryBtn=document.getElementById('clearHistoryBtn');

  // Simulated authenticated resident
  const resNameEl=document.getElementById('resName');
  const resLocationEl=document.getElementById('resLocation');
  const resAvatar=document.getElementById('resAvatar');
  const residentData={id:'res-1001',name:'María Pérez',tower:'A',apartment:'101'};
  if(resNameEl) resNameEl.textContent=residentData.name;
  if(resLocationEl) resLocationEl.textContent=`Torre ${residentData.tower} · Apt ${residentData.apartment}`;
  if(resAvatar) resAvatar.textContent=residentData.name.split(' ').map(s=>s[0]).slice(0,2).join('');

  const createQrImage=(text,size=260)=>{
    const image=new Image();
    image.alt='Código QR';
    image.src=`https://chart.googleapis.com/chart?cht=qr&chs=${size}x${size}&chl=${encodeURIComponent(text)}`;
    image.width=size;image.height=size;
    return image;
  };

  const formatDateTime=(iso)=>{
    if(!iso) return '-';
    const d=new Date(iso);
    return d.toLocaleString('es-CO',{day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
  };

  const uuid=()=>('id-'+Math.random().toString(36).slice(2,10));

  const saveIssuedVisit=(rec)=>{
    const raw=localStorage.getItem('issuedVisits');
    const arr=raw?JSON.parse(raw):[];
    arr.push(rec);
    localStorage.setItem('issuedVisits',JSON.stringify(arr));
  };

  const loadIssuedVisits=()=>{
    const raw=localStorage.getItem('issuedVisits');
    return raw?JSON.parse(raw):[];
  };

  const visitorProfilesKey='visitorProfiles';
  const loadVisitorProfiles=()=>{
    const raw=localStorage.getItem(visitorProfilesKey);
    return raw?JSON.parse(raw):[];
  };
  const saveVisitorProfiles=(profiles)=>{
    localStorage.setItem(visitorProfilesKey,JSON.stringify(profiles));
  };
  const addVisitorProfile=(name,document)=>{
    if(!name||!document) return;
    const profiles=loadVisitorProfiles();
    const normalizedDoc=document.trim();
    const index=profiles.findIndex(p=>p.document===normalizedDoc);
    const profile={name:name.trim(),document:normalizedDoc,lastVisit:new Date().toISOString()};
    if(index>-1){
      profiles[index]={...profiles[index],...profile};
    } else {
      profiles.unshift(profile);
    }
    saveVisitorProfiles(profiles.slice(0,20));
    populateVisitorDatalist();
  };
  const populateVisitorDatalist=()=>{
    if(!visitorList) return;
    const profiles=loadVisitorProfiles();
    visitorList.innerHTML=profiles.map(p=>`<option value="${p.name}"></option>`).join('');
  };
  const findVisitorProfile=(search)=>{
    if(!search) return null;
    const value=search.trim().toLowerCase();
    return loadVisitorProfiles().find(p=>p.name.toLowerCase()===value||p.document.toLowerCase()===value);
  };

  const updateActiveVisitsCount=()=>{
    const now=new Date();
    const count=loadIssuedVisits().filter(i=>!i.used && new Date(i.expiresAt)>now).length;
    if(activeVisitsCount) activeVisitsCount.textContent=count;
  };

  const loadVisitHistory=()=>{
    const raw=localStorage.getItem('visitHistory');
    const rows=raw?JSON.parse(raw):[];
    const tbody=document.querySelector('#visitHistoryTable tbody');
    if(!tbody) return;
    tbody.innerHTML='';
    rows.slice().reverse().forEach(rec=>{
      const tr=document.createElement('tr');
      const entry=formatDateTime(rec.entryTime);
      const exit=formatDateTime(rec.exitTime);
      const estado=rec.state==='Ingreso'?'<span class="badge badge-status active">Ingreso</span>':rec.state==='Salida'?'<span class="badge badge-status inactive">Salida</span>':rec.state==='Expirado'?'<span class="badge badge-status inactive">Expirado</span>':'<span class="badge badge-status inactive">'+(rec.state||'')+'</span>';
      tr.innerHTML=`<td>${rec.visitorName}</td><td>${rec.visitorDocument}</td><td>${rec.visitDate}</td><td>${rec.visitTime}</td><td>${estado}</td><td>${entry}</td><td>${exit}</td>`;
      tbody.appendChild(tr);
    });
  };

  if(validMinutes){
    validMinutes.addEventListener('change',()=>{
      if(validMinutes.value==='custom') customMinutesRow.classList.remove('hidden'); else customMinutesRow.classList.add('hidden');
    });
  }

  const syncVisitorDocument=()=>{
    const profile=findVisitorProfile(visitorName?.value||'');
    if(profile && visitorDocument) visitorDocument.value=profile.document;
  };

  const syncVisitorName=()=>{
    const profile=findVisitorProfile(visitorDocument?.value||'');
    if(profile && visitorName) visitorName.value=profile.name;
  };

  if(visitorName){
    visitorName.addEventListener('input',syncVisitorDocument);
  }
  if(visitorDocument){
    visitorDocument.addEventListener('input',syncVisitorName);
  }

  if(visitForm){
    visitForm.addEventListener('submit',e=>{e.preventDefault(); generateQrBtn.click();});
  }

  const clearAllHistory=()=>{
    if(confirm('¿Borrar historial de visitas y códigos emitidos?')){
      localStorage.removeItem('visitHistory');
      localStorage.removeItem('issuedVisits');
      loadVisitHistory();updateActiveVisitsCount();
      // clear preview
      if(qrPreview) qrPreview.innerHTML='<div class="qr-placeholder">Aún no hay QR</div>';
      if(qrState) qrState.textContent='—'; if(qrCreated) qrCreated.textContent='—'; if(qrExpires) qrExpires.textContent='—';
    }
  };
  if(clearHistoryBtn) clearHistoryBtn.addEventListener('click',clearAllHistory);

  if(generateQrBtn){
    generateQrBtn.addEventListener('click',()=>{
      const name=visitorName?.value.trim();
      const doc=visitorDocument?.value.trim();
      const dateVal=visitDate?.value;
      const timeVal=visitTime?.value;
      let minutes=Number(validMinutes?.value||0);
      if(validMinutes?.value==='custom') minutes=Number(customMinutes?.value||0);
      if(!name||!doc||!dateVal||!timeVal||!minutes){
        alert('Completa todos los campos y selecciona tiempo de vigencia.');
        return;
      }

      const issuedAt=new Date();
      const expiresAt=new Date(issuedAt.getTime()+minutes*60000);
      const tokenObj={
        tokenId:uuid(),
        residentId:residentData.id,
        residentName:residentData.name,
        tower:residentData.tower,
        apartment:residentData.apartment,
        visitorName:name,
        visitorDocument:doc,
        visitDate:dateVal,
        visitTime:timeVal,
        issuedAt:issuedAt.toISOString(),
        expiresAt:expiresAt.toISOString(),
        used:false
      };

      const tokenStr=btoa(unescape(encodeURIComponent(JSON.stringify(tokenObj))));
      const basePath=location.origin+location.pathname.replace(/[^/]*$/,'');
      const verifyUrl=`${basePath}visitas_validate.html?token=${encodeURIComponent(tokenStr)}`;

      // render QR preview
      if(qrPreview){qrPreview.innerHTML='';qrPreview.appendChild(createQrImage(verifyUrl,260));}
      if(qrState) qrState.textContent='Activo';
      if(qrCreated) qrCreated.textContent=formatDateTime(tokenObj.issuedAt);
      if(qrExpires) qrExpires.textContent=formatDateTime(tokenObj.expiresAt);

      // save issued
      saveIssuedVisit({
        tokenId:tokenObj.tokenId,
        visitorName:name,
        visitorDocument:doc,
        visitDate:dateVal,
        visitTime:timeVal,
        tower:residentData.tower,
        apartment:residentData.apartment,
        issuedAt:tokenObj.issuedAt,
        expiresAt:tokenObj.expiresAt,
        used:false
      });
      addVisitorProfile(name,doc);

      updateActiveVisitsCount();

      // download action
      if(downloadQrBtn){
        downloadQrBtn.onclick=()=>{
          const img=qrPreview.querySelector('img');
          if(!img) return alert('QR no disponible');
          const canvas=document.createElement('canvas');canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;const ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(img,0,0);const dataUrl=canvas.toDataURL('image/png');const a=document.createElement('a');a.href=dataUrl;a.download='qr_visit.png';a.click();
        }
      }

      if(shareQrBtn){
        shareQrBtn.onclick=async()=>{
          const url=verifyUrl;
          if(navigator.share){
            try{await navigator.share({title:'QR Visita',text:`QR para ${name}`,url});}catch(e){console.warn(e)}
          }else{
            navigator.clipboard.writeText(url).then(()=>alert('URL copiada al portapapeles'));
          }
        }
      }
    });
  }

  // initial load
  loadVisitHistory();
  updateActiveVisitsCount();
  populateVisitorDatalist();

  // Vehicles register
  const searchVeh=document.getElementById('searchVehicle');
  const vehiclesResultsCount=document.getElementById('vehiclesResultsCount');
  const vehicleModal=document.getElementById('vehicleModal');
  const addVehicleBtn=document.getElementById('addVehicleBtn');
  const closeVehicleModal=document.getElementById('closeVehicleModal');
  const cancelVehicleBtn=document.getElementById('cancelVehicleBtn');
  const vehicleForm=document.getElementById('vehicleForm');

  const loadVehicles=()=>{
    const raw=localStorage.getItem('vehiclesTable');
    return raw?JSON.parse(raw):[];
  };

  const saveVehicles=(vehicles)=>{
    localStorage.setItem('vehiclesTable',JSON.stringify(vehicles));
  };

  if(document.getElementById('vehiclesTableBody') && loadVehicles().length===0){
    saveVehicles([
      {plate:'ABC123',brand:'Toyota',model:'Corolla',color:'Blanco',cedula:'1001234567',ownerName:'Maria Perez',home:'Apto 101'}
    ]);
  }

  const renderVehicles=(vehicles)=>{
    const tbody=document.getElementById('vehiclesTableBody');
    if(!tbody) return;

    if(vehicles.length===0){
      tbody.innerHTML='<tr><td colspan="8" style="text-align:center;padding:40px;color:#999">Sin vehiculos aun</td></tr>';
      return;
    }

    tbody.innerHTML=vehicles.map(v=>`
      <tr>
        <td><strong>${v.plate}</strong></td>
        <td>${v.brand}</td>
        <td>${v.model}</td>
        <td>${v.color}</td>
        <td>${v.cedula||''}</td>
        <td>${v.ownerName||''}</td>
        <td>${v.home||''}</td>
        <td class="actions">
          <button class="action-btn delete-vehicle-btn" data-plate="${v.plate}" title="Eliminar">🗑</button>
        </td>
      </tr>
    `).join('');

    document.querySelectorAll('.delete-vehicle-btn').forEach(btn=>{
      btn.addEventListener('click',()=>{
        const plate=btn.dataset.plate;
        if(confirm('¿Eliminar este vehiculo?')){
          const updated=loadVehicles().filter(v=>v.plate!==plate);
          saveVehicles(updated);
          renderAndFilterVehicles();
        }
      });
    });
  };

  const renderAndFilterVehicles=()=>{
    const query=searchVeh?.value.toLowerCase()||'';
    const filtered=loadVehicles().filter(v=>{
      return !query ||
        v.plate.toLowerCase().includes(query) ||
        v.brand.toLowerCase().includes(query) ||
        v.model.toLowerCase().includes(query) ||
        v.color.toLowerCase().includes(query) ||
        (v.cedula||'').toLowerCase().includes(query) ||
        (v.ownerName||'').toLowerCase().includes(query) ||
        (v.home||'').toLowerCase().includes(query);
    });

    renderVehicles(filtered);
    if(vehiclesResultsCount){
      vehiclesResultsCount.textContent=`${filtered.length} resultado${filtered.length===1?'':'s'}`;
    }
  };

  const openVehicleModal=()=>{
    vehicleForm?.reset();
    vehicleModal?.classList.remove('hidden');
  };

  const closeVehicleModalWindow=()=>{
    vehicleForm?.reset();
    vehicleModal?.classList.add('hidden');
  };

  if(addVehicleBtn){
    addVehicleBtn.addEventListener('click',openVehicleModal);
  }
  if(closeVehicleModal){
    closeVehicleModal.addEventListener('click',closeVehicleModalWindow);
  }
  if(cancelVehicleBtn){
    cancelVehicleBtn.addEventListener('click',closeVehicleModalWindow);
  }
  if(vehicleModal){
    vehicleModal.addEventListener('click',e=>{
      if(e.target===vehicleModal) closeVehicleModalWindow();
    });
  }
  if(vehicleForm){
    vehicleForm.addEventListener('submit',e=>{
      e.preventDefault();
      const plate=document.getElementById('vehiclePlate').value.trim().toUpperCase();
      const brand=document.getElementById('vehicleBrand').value.trim();
      const model=document.getElementById('vehicleModel').value.trim();
      const color=document.getElementById('vehicleColor').value.trim();
      const cedula=document.getElementById('vehicleCedula').value.trim();
      const ownerName=document.getElementById('vehicleOwnerName').value.trim();
      const home=document.getElementById('vehicleHome').value.trim();

      if(!plate||!brand||!model||!color||!cedula||!ownerName||!home) return;

      const vehicles=loadVehicles();
      if(vehicles.some(v=>v.plate.toLowerCase()===plate.toLowerCase())){
        alert('Ya existe un vehiculo con esa placa.');
        return;
      }

      vehicles.push({plate,brand,model,color,cedula,ownerName,home});
      saveVehicles(vehicles);
      closeVehicleModalWindow();
      renderAndFilterVehicles();
    });
  }

  if(searchVeh){
    searchVeh.addEventListener('input',renderAndFilterVehicles);
  }

  renderAndFilterVehicles();
})
