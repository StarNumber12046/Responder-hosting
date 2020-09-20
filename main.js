const Discord = require('discord.js');
const MessageEmbed = require('discord.js');
 const client = new Discord.Client();

 
 client.on('ready', () => {
  client.user.setPresence({ activity: { name: 'r-aiutami / r-help' }, status: 'dnd' });
    console.log("avvio...1%...25%...50%...75%...100%...")
 

    


  })

client.on('message', msg => {
 if (msg.content === 'r-ping') {
 msg.reply('pong');
 }
 });
 client.on('message', msg => {
   if (msg.content === 'r-help'){
     msg.reply('Use ```r-aiutami```')
   }
   
 });

client.on('message', msg => {
  if(msg.content === 'r-ciao') {
    msg.channel.send('**AVE!** come va?')
  }
})
 client.on('message', msg => {
   if (msg.content === 'r-esplodi') {
     msg.channel.send('Esplodo')
     msg.react('🧨')
     console.log('sono esploso');
   }
 }																																																																							);
client.on('message', msg => {
  if(msg.content === 'r-ppolicy') {
    const embed = new Discord.MessageEmbed()
    // Set the title of the field
    .setTitle('Privacy Policy')
    .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')
    // Set the color of the embed
    .setColor('#00FFA6')
    // Set the main content of the embed
    .setDescription('**Raccolta Dati**\nNoi non raccogliamo nessun tipo di dato. I dati vengono elaborati e non registrati in alcun database e/o consolle\n**Uso dati**\nSiccome non raccogliamo dati non li utilizziamo in alcun modo\n**Gestione e visualizzazione dati**\nNon conserviamo dati quindi non è possibile gestirli o visualizzarli\n**Eliminazione dati**\nNon viene conservato alcun dato *quindi* non è possibile eliminarli');
  // Send the embed to the same channel as the message

  msg.channel.send(embed);
  }
})
client.on('message', msg => {
    if (msg.content === 'r-supporto') {
        msg.channel.send('https://discord.gg/WeBH4R2 <a:yep:722874462189650121>')
        msg.react('722874462189650121')
        
    }
})
client.on('message', msg => {
  if (msg.content === 'Ciao') {
      if (msg.channel.id === '714527883665735681')
      msg.channel.send('Salve a tutto lo staff!!')
  }
})
client.on('message', msg => {
  if(msg.channel.id === '714527942742507591') {
    msg.react('722874815886917702')
    msg.react('722874462189650121')
  }
})

 client.on('message', message =>{
   if (message.content === 'r-serverinfo') {
     const embed = new Discord.MessageEmbed()
     .setTitle('Statitiche server')
     .setDescription(`Nome server: ${message.guild.name}\nMembri totali: ${message.guild.memberCount}`)
     .setColor('#6400FF')
     .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')

     message.channel.send(embed)
   }
 });
 client.on('message', message =>{
   if (message.content === 'r-userinfo') {
     const embed = new Discord.MessageEmbed()
     .setTitle('I tuoi dati')
     .setDescription(`Nome utente: ${message.author.username}\nIl tuo id: ${message.author.id}`)
     .setColor('#FF5100')
     .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')
     message.channel.send(embed)
   }
 });

client.on('message', msg =>{
  if (msg.content === 'r-lol') {
    msg.channel.send('Non dire LOL, è meglio dire LEL!!!!!!!!')
  }
}); 
client.on('message', msg => {
  if(msg.content === 'r-lel') {
    msg.channel.send('Meglio LOL o LEL?')
    msg.react('1️⃣')
    msg.react('2️⃣')
  }
})

client.on('message', msg =>{
    if (msg.content === 'r-supportami') {
       msg.channel.send('Se ti piace il mio lavoro supportami invitandomi nel tuo server o regalando nitro a @StarNumber12046#9008')
    }
})
// Create an event listener for messages
client.on('message', message => {
  // If the message is "what is my avatar"
  if (message.content === 'r-avatar') {
    // Send the user's avatar URL
    message.reply(message.author.displayAvatarURL());
  }
});
client.on('message', msg => {
  if (msg.content === 'r-aiutami') {
    const embed = new Discord.MessageEmbed()
      // Set the title of the field
      .setTitle('COMANDI')
      .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')
      // Set the color of the embed
      .setColor('#00A6FF')
      // Set the main content of the embed
      .setDescription('ping : pong...\nciao : salve....\nesplodi : distruggimi, se hai il coraggio!\ninvito : invitami!\nlol : Lol...\nserverinfo : mostra info sul server dove si esegue il comando\nuserinfo : mostra info su di te\nsupportami : mostra come supportare me ed il mio autore!\nlel : meglio lol o lel?\navatar : mostra il tuo avatar\ninfo : mostra info sul bot\nppolicy : privacy policy richiesta da Discord\nsupporto : mostra il link al server di supporto');
    // Send the embed to the same channel as the message

    msg.channel.send(embed);
  }
});



  
client.on('message', msg => {
  if(msg.content === 'r-invito') {
    const embed = new Discord.MessageEmbed()
    // Set the title of the field
    .setTitle('Invito')
    .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')
    // Set the color of the embed
    .setColor('#FF8700')
    // Set the main content of the embed
    .setDescription('Davvero? Mi vuoi **INVITARE**?\nhttps://discord.com/api/oauth2/authorize?client_id=725342148488069160&permissions=8&scope=bot');
  // Send the embed to the same channel as the message

  msg.channel.send(embed);
  }
})
client.on('message', msg => {
  if (msg.content === '<@725342148488069160>') {
    msg.reply('**Il mio prefisso è r-**')
  }
})
client.on('message', msg => {
  if(msg.content === 'r-info') {
    const embed = new Discord.MessageEmbed()
    // Set the title of the field
    .setTitle('Info')
    .setAuthor('Command Responder', 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR_gfzqxgenIFs-ewjRZ9MOP0n91R_E6taIhQ&usqp=CAU')
    // Set the color of the embed
    .setColor('#FF8700')
    // Set the main content of the embed
    .setDescription('Developed by StarNumber12046#9008\nCo-Owner: XPower7125#5027\nSi ringraziano tutti coloro che hanno invitato e hanno riposto fiducia nel bot\nVersione Discord.js: 12.0.6');
  // Send the embed to the same channel as the message

  msg.channel.send(embed);
  }
})

client.login('NzI1MzQyMTQ4NDg4MDY5MTYw.XvNVhA.pr4oTJGyDpsMuNM-0ZjeLl2D1FI')
